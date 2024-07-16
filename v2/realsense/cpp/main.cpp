#define _WIN32_WINNT 0x0601 // Target Windows 7 or later
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <ctime>
#include <thread>
#include <queue>
#include <mutex>
#include <condition_variable>
#include <filesystem>
#include <atomic>
#include <chrono>
#include <cmath>
#include <algorithm>
#include <limits>
#include <vector>
#include <boost/asio.hpp>
#include <librealsense2/rs.hpp>
#include <Eigen/Dense>
#include <ogr_geometry.h>
#include <stdlib.h>

using namespace std::chrono;
namespace fs = std::filesystem;
using boost::asio::ip::tcp;

const std::string GPS_PORT = "COM4";
const int GPS_BAUD_RATE = 57600;
const double SENSOR_HEIGHT = 0.973; // Meters
const double SENSOR_TILT = 30; // Degrees
const double ANGLE_FROM_GPS = 270; // Degrees
const double DISTANCE_FROM_GPS = 0.4; // Meters
const double SENSOR_ORIENTATION = 2; // Degrees
const double MAX_DISTANCE_FROM_SENSOR = 4; // Meters
const double DOWNSCALE_FACTOR = 1;

class DataRecorder
{
public:
    DataRecorder() : start_time(system_clock::now()),
                     session_folder("data_" + currentDateTime()),
                     total_processing_time(0),
                     total_processed_frames(0),
                     min_processing_time(std::numeric_limits<double>::infinity()),
                     max_processing_time(0),
                     stop_event(false),
                     align_to_color(RS2_STREAM_COLOR)
    {
        fs::create_directory(session_folder);
        gps_file.open(session_folder + "/gps_data.txt");
        pointcloud_file.open(session_folder + "/pointcloud_data.npy", std::ios::binary);
        processed_file.open(session_folder + "/processed_data.txt");
        performance_file.open(session_folder + "/performance_data.txt");

        gps_thread = std::thread(&DataRecorder::gps_loop, this);
        realsense_thread = std::thread(&DataRecorder::realsense_loop, this);
        processing_thread = std::thread(&DataRecorder::processing_loop, this);
    }

    ~DataRecorder()
    {
        stop();
    }

    void start()
    {
        try
        {
            gps_thread.detach();
            realsense_thread.detach();
            processing_thread.detach();
            std::cout << "All threads started successfully." << std::endl;
        }
        catch (const std::exception &e)
        {
            std::cerr << "Error starting threads: " << e.what() << std::endl;
            stop();
        }
    }

    void stop()
    {
        stop_event = true;
        if (gps_thread.joinable())
            gps_thread.join();
        if (realsense_thread.joinable())
            realsense_thread.join();
        if (processing_thread.joinable())
            processing_thread.join();
        close();
    }

private:
    system_clock::time_point start_time;
    std::string session_folder;
    std::ofstream gps_file;
    std::ofstream pointcloud_file;
    std::ofstream processed_file;
    std::ofstream performance_file;
    std::vector<Eigen::Vector3d> latest_pointcloud;
    std::tuple<double, double, double, double> latest_gps;
    double current_heading;
    std::mutex pointcloud_lock;
    std::mutex gps_lock;
    std::queue<std::tuple<std::string, std::tuple<double, double, double, double>>> processing_queue;
    std::thread gps_thread;
    std::thread realsense_thread;
    std::thread processing_thread;
    rs2::pipeline pipeline;
    rs2::align align_to_color;
    std::atomic<bool> pipeline_started;
    std::mutex pipeline_lock;
    std::atomic<bool> stop_event;

    double total_processing_time;
    int total_processed_frames;
    double min_processing_time;
    double max_processing_time;

    static std::string currentDateTime()
    {
        auto now = std::chrono::system_clock::now();
        auto in_time_t = std::chrono::system_clock::to_time_t(now);
        struct tm timeinfo;
        localtime_s(&timeinfo, &in_time_t);
        std::stringstream ss;
        ss << std::put_time(&timeinfo, "%Y%m%d_%H%M%S");
        return ss.str();
    }

    void gps_loop()
    {
        try
        {
            boost::asio::io_service io_service;
            boost::asio::serial_port serial(io_service, GPS_PORT);
            serial.set_option(boost::asio::serial_port_base::baud_rate(GPS_BAUD_RATE));
            std::cout << "GPS connection established." << std::endl;

            while (!stop_event)
            {
                char c;
                std::string line;
                while (boost::asio::read(serial, boost::asio::buffer(&c, 1)) > 0 && c != '\n')
                {
                    line += c;
                }

                auto parsed_data = parse_nmea_data(line);
                if (std::get<0>(parsed_data) != 0)
                {
                    double timestamp = std::get<0>(parsed_data);
                    double lat = std::get<1>(parsed_data);
                    double lon = std::get<2>(parsed_data);
                    double heading = std::get<3>(parsed_data);
                    if (heading != 0)
                    {
                        current_heading = heading;
                    }
                    if (lat != 0 && lon != 0)
                    {
                        std::lock_guard<std::mutex> lock(gps_lock);
                        latest_gps = std::make_tuple(timestamp, lat, lon, current_heading);
                        gps_file << std::setprecision(15) << timestamp << "," << lat << "," << lon << "," << heading << std::endl;
                        gps_file.flush();
                        processing_queue.push(std::make_tuple("gps", latest_gps));
                    }
                }
            }
        }
        catch (const std::exception &e)
        {
            std::cerr << "GPS read error: " << e.what() << std::endl;
            stop_event = true;
        }
    }

    void realsense_loop()
    {
        try
        {
            rs2::config cfg;
            cfg.enable_stream(RS2_STREAM_DEPTH, 848, 480, RS2_FORMAT_Z16, 30);
            cfg.enable_stream(RS2_STREAM_COLOR, 848, 480, RS2_FORMAT_BGR8, 30);
            pipeline.start(cfg);
            pipeline_started = true;
            align_to_color = rs2::align(RS2_STREAM_COLOR);
            std::cout << "RealSense camera initialized successfully." << std::endl;

            while (!stop_event)
            {
                rs2::frameset frames = pipeline.wait_for_frames();
                frames = align_to_color.process(frames);

                rs2::frame depth_frame = frames.get_depth_frame();
                rs2::frame color_frame = frames.get_color_frame();

                if (!depth_frame || !color_frame)
                    continue;

                rs2::pointcloud pc;
                pc.map_to(color_frame);
                rs2::points points = pc.calculate(depth_frame);

                auto vertices = points.get_vertices();
                std::vector<Eigen::Vector3d> pointcloud;
                for (int i = 0; i < points.size(); ++i)
                {
                    pointcloud.push_back(Eigen::Vector3d(vertices[i].x, vertices[i].y, vertices[i].z));
                }

                std::lock_guard<std::mutex> lock(pointcloud_lock);
                latest_pointcloud = pointcloud;

                std::string filename = session_folder + "/pointcloud_" + std::to_string(std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch()).count()) + ".ply";
                points.export_to_ply(filename, color_frame);
            }
        }
        catch (const rs2::error &e)
        {
            std::cerr << "RealSense camera error: " << e.what() << std::endl;
        }
        stop_pipeline();
    }

    void stop_pipeline()
    {
        std::lock_guard<std::mutex> lock(pipeline_lock);
        if (pipeline_started)
        {
            try
            {
                pipeline.stop();
                pipeline_started = false;
                std::cout << "RealSense pipeline stopped successfully." << std::endl;
            }
            catch (const std::exception &e)
            {
                std::cerr << "Error stopping RealSense pipeline: " << e.what() << std::endl;
            }
        }
    }

    void processing_loop()
    {
        while (!stop_event)
        {
            try
            {
                if (!processing_queue.empty())
                {
                    auto item = processing_queue.front();
                    processing_queue.pop();
                    if (std::get<0>(item) == "gps")
                    {
                        auto process_start_time = system_clock::now();
                        double timestamp = std::get<0>(std::get<1>(item));
                        double lat = std::get<1>(std::get<1>(item));
                        double lon = std::get<2>(std::get<1>(item));
                        double heading = std::get<3>(std::get<1>(item));
                        std::lock_guard<std::mutex> lock(pointcloud_lock);
                        if (!latest_pointcloud.empty())
                        {
                            auto processed_pointcloud = process_pointcloud(latest_pointcloud, std::make_tuple(lat, lon, heading));

                            for (const auto &point : processed_pointcloud)
                            {
                                processed_file << std::setprecision(15) << point[0] << "," << point[1] << "," << point[2] << std::endl;
                            }
                            processed_file.flush();

                            auto process_end_time = system_clock::now();
                            auto processing_time = duration_cast<microseconds>(process_end_time - process_start_time).count();
                            auto total_time = duration_cast<microseconds>(process_end_time - start_time).count();
                            log_performance(timestamp, processing_time / 1000000.0, total_time / 1000000.0);
                            std::cout << "Processed and saved data for timestamp " << timestamp << std::endl;
                        }
                    }
                }
            }
            catch (const std::exception &e)
            {
                std::cerr << "Error in processing loop: " << e.what() << std::endl;
                if (stop_event)
                    break;
            }
        }
    }

    std::tuple<double, double, double, double> parse_nmea_data(const std::string &data)
    {
        std::stringstream ss(data);
        std::string item;
        std::vector<std::string> tokens;
        while (std::getline(ss, item, ','))
        {
            tokens.push_back(item);
        }
        std::string data_type = tokens[0].substr(1);

        if (data_type == "GNGGA" && tokens.size() >= 6)
        {
            try
            {
                double timestamp = duration_cast<milliseconds>(system_clock::now() - start_time).count() / 1000.0;
                double lat = std::stod(tokens[2].substr(0, 2)) + std::stod(tokens[2].substr(2)) / 60.0;
                if (tokens[3] == "S")
                    lat = -lat;
                double lon = std::stod(tokens[4].substr(0, 3)) + std::stod(tokens[4].substr(3)) / 60.0;
                if (tokens[5] == "W")
                    lon = -lon;

                if (lat < -90 || lat > 90 || lon < -180 || lon > 180)
                {
                    std::cerr << "Invalid GPS coordinates: " << lat << ", " << lon << std::endl;
                    return std::make_tuple(0, 0, 0, 0);
                }

                return std::make_tuple(timestamp, lat, lon, 0);
            }
            catch (const std::exception &e)
            {
                std::cerr << "Error parsing GNGGA data: " << e.what() << std::endl;
                return std::make_tuple(0, 0, 0, 0);
            }
        }
        else if (data_type == "GNRMC" && tokens.size() >= 9)
        {
            try
            {
                double timestamp = duration_cast<milliseconds>(system_clock::now() - start_time).count() / 1000.0;
                double heading = tokens[8].empty() ? 0 : std::stod(tokens[8]);
                return std::make_tuple(timestamp, 0, 0, heading);
            }
            catch (const std::exception &e)
            {
                std::cerr << "Error parsing GNRMC data: " << e.what() << std::endl;
                return std::make_tuple(0, 0, 0, 0);
            }
        }
        return std::make_tuple(0, 0, 0, 0);
    }

    std::vector<Eigen::Vector3d> process_pointcloud(const std::vector<Eigen::Vector3d> &pointcloud, const std::tuple<double, double, double> &gps_data)
    {
        const double voxel_size = 0.05; // 5cm voxel size
        std::map<std::tuple<int, int, int>, Eigen::Vector3d> voxel_grid;
        for (const auto &point : pointcloud)
        {
            auto voxel_key = std::make_tuple(
                static_cast<int>(std::floor(point[0] / voxel_size)),
                static_cast<int>(std::floor(point[1] / voxel_size)),
                static_cast<int>(std::floor(point[2] / voxel_size)));
            if (voxel_grid.find(voxel_key) == voxel_grid.end() || point[2] < voxel_grid[voxel_key][2])
            {
                voxel_grid[voxel_key] = point;
            }
        }
        std::vector<Eigen::Vector3d> downsampled_pointcloud;
        for (const auto &voxel : voxel_grid)
        {
            downsampled_pointcloud.push_back(voxel.second);
        }

        double lat = std::get<0>(gps_data);
        double lon = std::get<1>(gps_data);
        double heading = std::get<2>(gps_data);
        std::cout << "GPS data: " << std::setprecision(15) << lat << ", " << std::setprecision(15) << lon << ", " << heading << std::endl;

        if (lat == 0 && lon == 0)
        {
            std::cerr << "Invalid GPS data. Skipping point cloud processing." << std::endl;
            return std::vector<Eigen::Vector3d>();
        }

        double easting = 0, northing = 0;
        OGRSpatialReference sr;
        sr.SetWellKnownGeogCS("WGS84");
        OGRSpatialReference utm;
        int zone = static_cast<int>((lon + 180) / 6) + 1;
        utm.SetUTM(zone, lat >= 0);
        OGRCoordinateTransformation *transform = OGRCreateCoordinateTransformation(&sr, &utm);
        if (transform && transform->Transform(1, &lat, &lon))
        {
            easting = lon;
            northing = lat;
        }
        else
        {
            std::cerr << "Transformation error: " << CPLGetLastErrorMsg() << std::endl;
            easting = lon;
            northing = lat;
        }

        OGRCoordinateTransformation::DestroyCT(transform);

        Eigen::Matrix3d R_tilt = Eigen::AngleAxisd(-(SENSOR_TILT+90) * M_PI / 180, Eigen::Vector3d::UnitX()).toRotationMatrix();
        Eigen::Matrix3d R_orientation = Eigen::AngleAxisd((SENSOR_ORIENTATION + heading) * M_PI / 180, Eigen::Vector3d::UnitZ()).toRotationMatrix();
        Eigen::Matrix3d R = R_orientation * R_tilt;

        std::vector<Eigen::Vector3d> transformed_points;
        for (const auto &point : downsampled_pointcloud)
        {
            Eigen::Vector3d transformed_point = R * point;
            transformed_point[0] += DISTANCE_FROM_GPS * std::sin((ANGLE_FROM_GPS + heading) * M_PI / 180);
            transformed_point[1] += DISTANCE_FROM_GPS * std::cos((ANGLE_FROM_GPS + heading) * M_PI / 180);
            transformed_point[2] += SENSOR_HEIGHT;
            double distance = transformed_point.norm();
            if (distance <= MAX_DISTANCE_FROM_SENSOR)
            {
                transformed_point[0] += easting;
                transformed_point[1] += northing;
                if (std::isfinite(transformed_point[0]) && std::isfinite(transformed_point[1]) && std::isfinite(transformed_point[2]))
                {
                    transformed_points.push_back(transformed_point);
                }
                else
                {
                    std::cerr << "Invalid transformed point: " << transformed_point.transpose() << std::endl;
                }
            }
        }
        return transformed_points;
    }

    void log_performance(double timestamp, double processing_time, double total_time)
    {
        total_processing_time += processing_time;
        total_processed_frames++;
        min_processing_time = std::min(min_processing_time, processing_time);
        max_processing_time = std::max(max_processing_time, processing_time);
        double avg_processing_time = total_processing_time / total_processed_frames;

        std::stringstream ss;
        ss << "Timestamp: " << timestamp << ", "
           << "Processing Time: " << processing_time << "s, "
           << "Total Time: " << total_time << "s, "
           << "Avg Processing Time: " << avg_processing_time << "s, "
           << "Min Processing Time: " << min_processing_time << "s, "
           << "Max Processing Time: " << max_processing_time << "s" << std::endl;

        performance_file << ss.str();
        performance_file.flush();
        std::cout << ss.str();
    }

    void close()
    {
        std::cout << "Closing connections and files..." << std::endl;
        stop_pipeline();
        if (gps_file.is_open())
            gps_file.close();
        if (pointcloud_file.is_open())
            pointcloud_file.close();
        if (processed_file.is_open())
            processed_file.close();
        if (performance_file.is_open())
            performance_file.close();
        std::cout << "All connections and files closed." << std::endl;
    }
};

void main_loop()
{
    while (true)
    {
        std::cout << "Enter 'R' to record new data, 'Q' to quit: ";
        char key;
        std::cin >> key;
        key = std::toupper(key);

        if (key == 'R')
        {
            DataRecorder recorder;
            try
            {
                recorder.start();
                std::cout << "Press Enter to stop recording...\n";
                std::cin.ignore();
                std::cin.get();
            }
            catch (const std::exception &e)
            {
                std::cerr << "Error during recording: " << e.what() << std::endl;
            }
            recorder.stop();
        }
        else if (key == 'Q')
        {
            break;
        }
        else
        {
            std::cerr << "Invalid choice. Please try again." << std::endl;
        }
    }
}

int main()
{
    const char *proj_path = "C:\\OSGeo4W\\share\\proj";
    _putenv_s("PROJ_LIB", proj_path);
    main_loop();
    return 0;
}
