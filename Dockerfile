FROM osrf/ros:humble-desktop

# Core System Utilities
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    lsb-release \
    python3-pip \
    python3-colcon-common-extensions \
    nano \
    tmux \
    xterm \
    tree \
    libgl1-mesa-glx \
    libgl1-mesa-dri \
    libgles2-mesa \
    mesa-utils \
    && rm -rf /var/lib/apt/lists/*

# Gazebo Ignition Fortress Installation
RUN curl https://packages.osrfoundation.org/gazebo.gpg --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] https://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null && \
    apt-get update && apt-get install -y \
    ignition-fortress \
    ros-humble-ros-gz \
    ros-humble-ros2-control \
    ros-humble-ros2-controllers \
    ros-humble-ign-ros2-control \
    && rm -rf /var/lib/apt/lists/*

# Copy uv binaries directly from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Use uv to install global system packages
RUN uv pip install --system \
    "setuptools<70.0.0" \
    "numpy<1.25.0" \
    trimesh \
    qrcode[pil] \
    transforms3d \
    && uv pip uninstall --system matplotlib
    
# ROS 2 Package Dependencies
RUN apt-get update && apt-get install -y \
    ros-humble-joint-state-publisher \
    ros-humble-navigation2 \
    ros-humble-nav2-bringup \
    ros-humble-twist-mux \
    ros-humble-twist-stamper \
    ros-humble-teleop-twist-keyboard \
    ros-humble-joy \
    ros-humble-joy-teleop \
    ros-humble-robot-state-publisher \
    ros-humble-tf-transformations \
    ros-humble-xacro \
    ros-humble-cv-bridge \
    python3-opencv \
    ros-humble-rviz2 \
    ros-humble-rqt \
    ros-humble-rqt-common-plugins \
    ros-humble-rqt-tf-tree \
    ros-humble-rqt-graph \
    ros-humble-rqt-image-view \
    ros-humble-foxglove-bridge \
    ros-humble-foxglove-msgs \
    python3-yaml \
    && rm -rf /var/lib/apt/lists/*

# Environment Variables for Software Rendering and Display
ENV LIBGL_ALWAYS_SOFTWARE=1
ENV MESA_GL_VERSION_OVERRIDE=3.3

# Workspace Setup
RUN echo 'for gid in $(id -G); do getent group $gid >/dev/null || groupadd -g $gid host_group_$gid 2>/dev/null; done' >> /root/.bashrc && \
    echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc && \
    echo "if [ -f /root/puzzlebot-sim/ros2_ws/install/setup.bash ]; then source /root/puzzlebot-sim/ros2_ws/install/setup.bash; fi" >> /root/.bashrc && \
    echo "" >> /root/.bashrc && \
    echo 'find /root/puzzlebot-sim -type f \( -name "*.py" -o -name "*.sh" -o -name "*.bash" \) -exec chmod +x {} + 2>/dev/null' >> /root/.bashrc && \
    echo "" >> /root/.bashrc && \
    echo "# Core Aliases" >> /root/.bashrc && \
    echo "alias cb='rm -rf log build install && colcon build && source install/setup.bash'" >> /root/.bashrc && \
    echo "alias simulation_puzzlebot='ros2 launch puzzlebot_bringup simulation_puzzlebot.launch.py'" >> /root/.bashrc && \
    echo "alias puzzlebot='ros2 launch puzzlebot_bringup puzzlebot.launch.py'" >> /root/.bashrc && \
    echo "alias display_rviz='ros2 launch puzzlebot_description display_rviz.launch.py'" >> /root/.bashrc && \
    echo "alias simulation_gazebo='ros2 launch puzzlebot_description simulation_gazebo.launch.py'" >> /root/.bashrc && \
    echo "" >> /root/.bashrc && \
    echo "# Lock Aliases" >> /root/.bashrc && \
    echo "alias lock_robot='ros2 topic pub --once /lock std_msgs/msg/Bool \"{data: true}\"'" >> /root/.bashrc && \
    echo "alias unlock_robot='ros2 topic pub --once /lock std_msgs/msg/Bool \"{data: false}\"'" >> /root/.bashrc && \
    echo "alias lock_forks='ros2 topic pub --once /forklift_controller/lock std_msgs/msg/Bool \"{data: true}\"'" >> /root/.bashrc && \
    echo "alias unlock_forks='ros2 topic pub --once /forklift_controller/lock std_msgs/msg/Bool \"{data: false}\"'" >> /root/.bashrc
    
WORKDIR /root/puzzlebot-sim/ros2_ws

CMD ["bash"]