> [!IMPORTANT]
> For complete understanding and proper operation of this repository's code, please read this README file in its entirety and follow the instructions step by step.

# Puzzlebot Simulation for Autonomous Navigation on a Smart Factory

<p align="justify">
Main project developed in collaboration with <i>E80 Group</i> and <i>Manchester Robotics</i> (<i>MCR2</i>) as part of the undergraduate course <i>"Integration of Robotics and Intelligent Systems"</i> in the <i>B.S. in Robotics and Digital Systems Engineering</i> program at the <i>Instituto Tecnológico y de Estudios Superiores de Monterrey</i> (<i>ITESM</i>), Mexico.
</p>

<p align="justify">
<img width="13393" height="2224" alt="sponsor_logos" src="https://github.com/user-attachments/assets/a42d8e52-74bb-43de-bb66-7812463216cd" />
</p>

<p align="justify">
The <i>Puzzlebot</i> is a <i>differential-drive</i> educational robot developed by Manchester Robotics. To mirror the real-world applications of E80 Group—a global company specialized in automated intralogistics solutions and the development of Industry 4.0 Smart Factories—this project required transforming the platform into an <i>Autonomous Mobile Robot</i> (<i>AMR</i>).
</p>

<p align="center">
<img width="500" height="282.5" alt="puzzlebot" src="https://github.com/user-attachments/assets/b702ff98-e421-4be5-8baa-9100578ed1d6" />
<br>
<em>Puzzlebot</em>
</p>

<p align="justify">
By retrofitting the Puzzlebot with a custom <i>forklift</i> mechanism, the adapted robot must navigate a physical mock-up of a smart factory known as <i>RoboArena 4.0</i> to execute basic intralogistics flows. There is a set of ArUco markers available on the walls that can help with the task. Relying on its onboard sensors, the main objective is for the robot to autonomously identify, pick up, transport, and deposit pallets within the arena.
</p>

<p align="center">
<img width="960" height="540" alt="puzzlebotforkliftpallets" src="https://github.com/user-attachments/assets/de2b78df-e83b-4d13-9c31-487f00a7e694" />
</p>

<p align="justify">
Specifically, there are two core missions: loading a trailer from the end-of-line conveyors and loading a trailer from the storage shelves or racks. For both missions, the robot is required to explore the designated area to locate a target pallet with a visible QR code, align itself correctly to read the client data, and carefully execute a final approach to pick up the pallet using its forks.
</p>

<p align="center">
<img width="624" height="431.5" alt="roboarenamap" src="https://github.com/user-attachments/assets/d0365de1-43bd-45ea-a446-9df7826f09fd" />
<br>
<em>RoboArena 4.0 Map</em>
</p>

<p align="center">
<img width="624" height="380.3" alt="roboarena" src="https://github.com/user-attachments/assets/ea9abd14-e007-4d09-b53f-8c9840c1201e" />
<br>
<em>RoboArena 4.0</em>
</p>

<p align="justify">
Once the pallet is secured, the robot must navigate to the shipping area and visually match the extracted QR data with the corresponding client logo displayed on the available trailers. Finally, the system must drive into the correct dock, deposit the pallet on the floor, and safely exit the trailer to complete the autonomous operation.
</p>

<p align="center">
<img width="624" height="200" alt="trailer_logos" src="https://github.com/user-attachments/assets/a1a220cf-429f-4cf5-ae1d-333e989f3be4" />
<br>
<em>Client Logos: Emezon, Wolmar, & Popsi</em>
</p>

<p align="center">
<img width="504" height="532.5" alt="aigeneratedroboarena" src="https://github.com/user-attachments/assets/94dfe705-32d5-4be4-99d4-d99304355496" />
<br>
<em>RoboArena 4.0 AI Concept Art</em>
</p>

## About

<p align="justify">
This repository contains a <i>1:1 Digital Twin simulation of the E80 RoboArena 4.0</i> built completely from scratch in <code>Gazebo Fortress</code> and <code>ROS 2 Humble Hawksbill</code>, recreating both the fully operable Puzzlebot with a forklift and the complete factory layout with accurate physics, enabling realistic interactions between the robot and the facility infrastructure:</p>

<ul>
  <li>End-of-line <i>conveyors</i>.</li>
  <li><i>Storage shelves</i> or <i>racks</i>.</li>
  <li><i>Client logos</i> on the <i>trailers</i>.</li>
  <li><i>Pallets</i> supporting <i>QR cubes</i>.</li>
  <li><i>ArUco markers</i> on the walls.</li>
</ul>

<p align="center">
<img width="410" height="257" alt="rosgazebo" src="https://github.com/user-attachments/assets/ead839e9-43f7-4cc8-8adc-5e2d798ebe66" />
</p>

<p align="center">
<img width="1788" height="1209" alt="simroboarenamap" src="https://github.com/user-attachments/assets/eb5185e4-7643-4404-b9f7-d10de8425844" />
<br>
<em>Simulation RoboArena 4.0 Map</em>
</p>

<p align="center">
<img width="1985" height="880" alt="simroboarena" src="https://github.com/user-attachments/assets/c765f57f-b582-4e38-b4f9-63aeeb098413" />
</p>

<p align="justify">
It is possible to validate algorithms (<i>Simultaneous Localization and Mapping</i> (<i>SLAM</i>), <i>Monte Carlo Localization</i>, <i>QR/ArUco reading</i>, <i>A* with Costmap</i>, <i>Pure Pursuit</i>, and <i>Open-Loop Position Control</i>) prior to physical deployment by employing high-fidelity dynamics alongside precise sensor simulations (<i>LiDAR</i> and <i>camera</i>).
</p>

<p align="center">
<img width="1985" height="880" alt="simroboarenalidar" src="https://github.com/user-attachments/assets/21dab8cc-2d14-4c1b-a753-b58f8d4df807" />
</p>

<p align="justify">
The <code>ROS 2</code> software is containerized using <code>Docker Compose</code>, guaranteeing a reproducible, cross-platform, and hardware-accelerated (NVIDIA GPU) development workspace.
</p>

<p align="justify">
<img width="2460" height="460" alt="dockernvidialogos" src="https://github.com/user-attachments/assets/f00b1a55-dd1b-457c-9f8d-0a28da8bf5f3" />
</p>

It is linked to a <code>Foxglove</code> controller, enabling real-time telemetry visualization and direct remote operation. 

<p align="center">
<img width="427" height="79" alt="foxglovelogo" src="https://github.com/user-attachments/assets/4f975ffe-9e6b-4d60-8a35-b54adf344e45" />
</p>

<p align="justify">
<img width="2549" height="1411" alt="foxglovepanel" src="https://github.com/user-attachments/assets/64b4ab56-fb20-47cf-bc22-daba6d94c914" />
</p>

<p align="justify">
It maintains identical <code>ROS 2</code> software architectures for both the physical and simulated counterparts, which means that all the code written for the simulation can be directly used in the real robot with no modifications or only minor tweaks.
</p>

## Installation

<p align="justify">The software in this repository is built on <code>ROS 2 Humble Hawksbill</code>, which natively targets <code>Ubuntu 22.04 LTS (Jammy Jellyfish)</code>. Since initial development occurred on <code>Ubuntu 26.04 LTS (Resolute Raccoon)</code>, <code>Docker</code> is utilized to provide a containerized environment. This approach ensures a consistent, reproducible <code>ROS 2</code> setup across different host operating systems while avoiding dependency conflicts.</p>

### Hardware Acceleration Requirements (Optional)

<p align="justify">Hardware acceleration is recommended to improve the performance of <code>Gazebo Fortress</code> simulation. This setup was explicitly tested using an <code>NVIDIA GeForce RTX 4060</code> GPU. If a dedicated NVIDIA GPU is unavailable, this section can be skipped, and the CPU-only configuration can be used instead.</p>

<p align="justify">The host machine must have proprietary NVIDIA drivers installed and loaded. Refer to the official installation guidelines for the specific Linux distribution.</p>

<p align="justify">For <a href="https://ubuntu.com/server/docs/how-to/graphics/install-nvidia-drivers/">Ubuntu</a>  systems, drivers are typically installed via the following commands:</p>

```bash
sudo ubuntu-drivers install
sudo reboot
```

<p align="justify">Verify the installation by checking the GPU model and CUDA version:</p>

```bash
nvidia-smi
```

<p align="justify">Do not proceed with the GPU-accelerated setup if this command fails to output the device table.</p>

### Docker Setup

<p align="justify">Install <code>Docker Engine</code> and the <code>Docker Compose</code> plugin according to the official documentation for the host system:</p>

<ul>
  <li>
    <p align="justify">
      <a href="https://docs.docker.com/engine/install/">Docker Engine Installation Guide</a>
    </p>
  </li>
  <li>
    <p align="justify">
      <a href="https://docs.docker.com/engine/install/linux-postinstall">Linux Post-Installation Steps for Docker Engine</a>
    </p>
  </li>
  <li>
    <p align="justify">
      <a href="https://docs.docker.com/compose/install/linux/">Docker Compose Installation Guide</a>
    </p>
  </li>
</ul>
<p align="justify">If utilizing NVIDIA GPU acceleration, the <code>NVIDIA Container Toolkit</code> must also be installed to allow <code>Docker</code> to interface with the host's GPU hardware:</p>

<ul>
  <li>
    <p align="justify">
      <a href="https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html">NVIDIA Container Toolkit Installation Guide</a>
    </p>
  </li>
</ul>

### Repository Initialization

<p align="justify">Clone the repository and navigate to the root directory containing the <code>Docker</code> configuration files:</p>

```bash
git clone https://github.com/fectec/puzzlebot-sim.git
cd puzzlebot-sim
```

### Graphical Interface Permissions

<p align="justify">Prior to starting the container, you must grant the local <code>Docker</code> user access to the host's X server. This is mandatory for rendering graphical interfaces, such as <code>Gazebo</code> and <code>RViz</code>, from within the container. Note that this permission is temporary and resets every time you reboot your host machine.</p>

<p align="justify">To make this permanent and avoid having to authorize it on every boot, append the command to your host's <code>~/.bashrc</code> file by running the following command once:</p>

```bash
echo "xhost +local:docker > /dev/null" >> ~/.bashrc
source ~/.bashrc
```

<p align="justify">If you prefer not to modify your bash profile, you will need to run the authorization manually every time you restart your computer before launching the container:</p>

```bash
xhost +local:docker
```

<p align="justify">If your Linux distribution strictly enforces Wayland without Xwayland support, you might encounter "Cannot connect to display" errors when launching graphical interfaces like <code>Gazebo</code>. To resolve this, you can switch back to the classic X11 display server:</p>

<ol>
  <li>Log out of your current user session.</li>
  <li>On the login screen, click your username.</li>
  <li>Before entering your password, click the gear icon in the bottom right corner and select "Ubuntu on Xorg" (or your distro's equivalent).</li>
</ol>

<p align="justify">Ubuntu 26.04 LTS (Resolute Raccoon) has completely dropped the native X11 session option. Wayland is now the sole display protocol, and all system graphical applications run via Wayland by default. Legacy applications that still require X11 (such as <code>Gazebo</code> and <code>RViz</code>) will automatically execute through the built-in XWayland compatibility layer, so no further configuration is required.</p>

### Container Deployment

<p align="justify">Build and start the container in detached mode. Depending on the available hardware, select the appropriate configuration:</p>

<p align="justify">For GPU-accelerated environments:</p>

```bash
docker compose -f docker-compose.yml -f docker-compose.gpu.yml up -d --build
```

<p align="justify">For CPU-only environments:</p>

```bash
docker compose up -d --build
```

<p align="justify">Access the interactive bash shell inside the running container using the following command. The default working directory is internally mapped to <code>/root/puzzlebot-sim/ros2_ws</code>. 

```bash
docker exec -it puzzlebot-sim_container bash
```

To exit the container and return to the host terminal, type <code>exit</code> and press Enter.</p>

### ROS 2 Workspace Workflow

<p align="justify">The entire <code>puzzlebot-sim</code> directory from the host is mounted directly at <code>/root/puzzlebot-sim</code> inside the container. Any modifications made to the source files on the host machine are immediately reflected internally, and vice versa.</p>

<p align="justify">The standard build and execution process inside the container shell is as follows:</p>

```bash
# The base ROS 2 environment is sourced automatically via ~/.bashrc.
cd /root/puzzlebot-sim/ros2_ws
colcon build
source install/setup.bash
ros2 launch <package_name> <launch_file.launch.py>
```

Or alternatively, use the <code>cb</code> alias:

```bash
cd /root/puzzlebot-sim/ros2_ws
cb
ros2 launch <package_name> <launch_file.launch.py>
```

### Container Lifecycle Management

<p align="justify">Use the following commands from the repository root on the host machine to manage the container state.</p>

#### Stopping and Starting

<p align="justify">To pause the container without destroying its internal state, allowing it to be resumed later:</p>

```bash
docker compose stop
docker compose start
```

#### Applying Configuration Changes (No Rebuild)

<p align="justify">To apply modifications made to the <code>docker-compose.yml</code> or <code>docker-compose.gpu.yml</code> files when the <code>Dockerfile</code> has not been altered. <code>Docker Compose</code> will automatically detect the changes and recreate the container while bypassing a full image rebuild:</p>

For GPU-accelerated environments:

```bash
docker compose -f docker-compose.yml -f docker-compose.gpu.yml up -d
```

For CPU-only environments:

```bash
docker compose up -d
```

#### Deep Clean

<p align="justify">To completely tear down the container and reset the environment. This procedure is recommended when performing a fresh setup, troubleshooting persistent issues, or completely removing the container's state from the host machine:</p>

For GPU-accelerated environments:

```bash
docker compose -f docker-compose.yml -f docker-compose.gpu.yml down
```

For CPU-only environments:

```bash
docker compose down
```

### Auto-Start on System Boot

<p align="justify">By default, <code>Docker</code> containers remain inactive after restarting your host machine. Normally, this would force you to manually run <code>docker compose start</code> every time you boot up your computer before you can access the container.</p>

<p align="justify">To streamline the workflow, the <code>docker-compose.yml</code> file includes the <code>restart: unless-stopped</code> policy. This configuration tells <code>Docker</code> to automatically wake up the <code>puzzlebot-sim_container</code> as soon as you turn on your computer, allowing you to jump straight into the terminal using the <code>docker exec -it puzzlebot-sim_container</code> bash command. The container will only stay offline if you explicitly stopped it (using <code>down</code> or <code>stop</code>) before shutting down the machine.</p>

<p align="justify">For this policy to work, the <code>Docker Engine</code> daemon must be configured to start automatically when your Linux system boots. If the <code>Docker Engine</code> is off, it cannot read the compose file to start your container.</p>

<p align="justify">To ensure the <code>Docker</code> service starts on boot, run the following commands once on your host machine terminal:</p>

```bash
sudo systemctl enable docker
sudo systemctl enable containerd
```

## First Steps

This section is designed to let you dive right in to explore and test the simulation. However, for further development, reading the next section is mandatory.

### Teleoperation

<p align="justify">First, download and install <code>Foxglove Studio</code> from their official website:</p>

<ul>
  <li>
    <p align="justify">
      <a href="https://foxglove.dev/download">Foxglove Studio Installation Guide</a>
    </p>
  </li>
</ul>

<p align="justify">After completing the standard build process inside the container shell (refer to the <i>ROS 2 Workspace Workflow</i> section), you can execute the launch command to start the simulation:</p>

```bash
ros2 launch puzzlebot_bringup simulation_puzzlebot.launch.py
```

<p align="justify">Alternatively, you can use the provided alias:</p>

```bash
simulation_puzzlebot
```

<p align="justify">This will open both <code>Gazebo</code> and <code>RViz</code> windows. Next, open <code>Foxglove</code> on your host computer (not inside the <code>Docker</code> container) using either the GUI application or your terminal:</p>

```bash
foxglove-studio
```

<p align="justify">Click <code>Open connection</code> on the <code>Dashboard</code>, which will prompt an <code>Open a new connection</code> window. Search for <code>Foxglove WebSocket</code>, and inside the <code>WebSocket URL</code> text box, enter the default local host address and port (this default setting can be modified, which will be explored later).</p>

```bash
ws://localhost:8765
```

> [!NOTE]
> Official documentation may suggest installing the foxglove_bridge ROS package, but this is unnecessary as it is already fully integrated into the Docker image.

<p align="justify">Click <code>Open</code>. If successful, navigate to the upper right corner of the window, click <code>Select a layout</code>, then <code>Import from file</code>. Locate the <code>puzzlebot-sim/ros2_ws/puzzlebot_bringup/foxglove_config</code> folder from the cloned repository and select the corresponding <code>display_foxglove.json</code> layout file. This will load the custom <code>Foxglove</code> panel specifically configured for this codebase.</p>

<p align="justify">Here, you will find a <code>Control Panel</code> with teleoperation functions for both the Puzzlebot and the forklift mechanism:</p>

<ul>
  <li>
    <p align="justify"><i>Puzzlebot</i>: The Up and Down buttons control the linear X velocity, while the Left and Right buttons control the angular Z velocity.</p>
  </li>
    <li>
    <p align="justify"><i>Forks</i>: The Up and Down buttons control the elevation of the forks. The Left and Right buttons do nothing.</p>
  </li>
</ul>

<p align="center">
<img width="238.5" height="373" alt="teleopfoxglove" src="https://github.com/user-attachments/assets/da4e4a96-8264-483d-ae8a-a08140bd221e" />
</p>

<p align="justify">This is the easiest way to manually move the robot and the forks. Try it out, and you will see the robot and forks moving in the <code>Gazebo</code> window.</p>

<p align="center">
<img width="426" height="240" alt="movementgazebo" src="https://github.com/user-attachments/assets/303e6048-ef93-40e2-aeb9-0cb09f61a3dd" />
</p>

<p align="justify">These movements will also be reflected in the <code>Computer Vision Panel</code>. You will see a live feed from the robot's primary camera (<code>Raw Vision</code>) as well as a feed from a camera mounted directly on the forks. Note that this fork-mounted camera does not technically exist on the physical robot; it was added strictly for debugging purposes (<code>Debug Camera (Forks-Eye View)</code>).</p>

<p align="justify">In the <code>Motion Status Panel</code>, you will see dial gauges and real-time plots for the robot's linear X and angular Z velocities. There is also a bar gauge representing the forklift's elevation level—empty when at its lowest position and full when at its highest. These visualizers will update dynamically as you teleoperate the system.</p>

<p align="center">
<img width="240" height="360" alt="movement" src="https://github.com/user-attachments/assets/23be4fda-9537-40e5-8102-d0d15b194d7d"/>
</p>

<p align="justify">Optionally, if you have a physical gamepad, you can use it for teleoperation. This setup was specifically mapped for the <code>8BitDo Ultimate 2C Controller</code>, but it should work right out of the box with most standard joysticks (like an Xbox controller). If it does not behave as expected, the next section will explain how to fix or customize the teleoperation mappings.</p>

<p align="justify">By default, the <code>Right Bumper (RB)</code> acts as a "<i>deadman switch</i>." For safety reasons, you must hold this button down for the Puzzlebot to move. The moment you release it, the robot will stop entirely, even if you are providing movement input on the sticks. Note that this safety switch does not lock the forks.</p>

<p align="justify">The <code>Left Analog Stick (LSB)</code> controls the linear X velocity, and the <code>Right Analog Stick (RSB)</code> controls the angular Z velocity. The <code>Up</code> and <code>Down</code> buttons on the <code>D-PAD</code> control the fork elevation.</p>

<p align="center">
<img width="600" height="322" alt="joystick" src="https://github.com/user-attachments/assets/701f28ad-6370-4321-84b4-b96a3fdb2726" />
</p>

<p align="justify">For added security, the <code>Control Panel</code> includes <code>Lock</code> and <code>Unlock</code> buttons for both the Puzzlebot and the forks. If you engage the <code>Lock</code>, all movement will cease, and you will be completely unable to move the robot or the forks (this overrides both manual teleoperation and autonomous behaviors). Use the <code>Unlock</code>button to remove this restriction and resume movement.</p>

<p align="justify">Finally, you will notice a <code>Forklift Status</code> indicator panel that displays the current operational state of the forklift controller. More details on this will be covered in the next section.</p>

<p align="center">
<img width="240" height="327" alt="controlpanel" src="https://github.com/user-attachments/assets/50b6902c-a849-42ef-a03f-32585d2ca7e3" />
</p>

### Navigation

<p align="justify"><code>Nav2</code> is the professionally supported Navigation Stack for <code>ROS 2</code>. The simulation incorporates a <code>Nav2 Map Server</code> that broadcasts a pre-mapped layout of the simulated factory on the <code>/map</code> topic. This static map uses a standard <code>Occupancy Grid</code> grayscale representation: white pixels indicate free, navigable space; black pixels represent solid obstacles (like walls or racks); and gray pixels represent unknown or unmapped areas.</p>

<p align="justify">Additionally, a <code>Nav2 Costmap</code> node publishes data on the <code>/costmap/costmap</code> topic. The costmap takes the static black-and-white map and applies "inflation layers" around all the obstacles. This ensures the robot maintains a safe buffer distance to avoid collisions. Visually, this is represented by vibrant color gradients (often light blue, purple, and red), where warmer colors indicate a higher "cost" penalty and closer proximity to a physical obstacle.</p>

<p align="justify">To localize the robot within this map, the system uses an <code>Nav2 Adaptive Monte Carlo Localization (AMCL)</code> node. In simple terms, <code>AMCL</code> probabilistically estimates the robot's exact location by constantly comparing the live laser scans from the LiDAR (published on the <code>/scan</code> topic) against the known static map walls, while also factoring in the robot's continuous odometry data to track movement between those scans.</p>

<p align="justify">In the <code>RViz</code> window and the right-side <code>Foxglove</code> panels (<code>RoboArena 4.0</code> & <code>RoboArena 4.0 Bird's-Eye View</code>), you will see a rendering of both the map and the costmap. Because the costmap overlaps the static map, you will easily recognize it by its vibrant colors. In both the <code>RViz</code> and <code>Foxglove</code> settings, you can hide the costmap to reveal the plain, grayscale static map underneath. You will also see blue spheres, which represent the live points where the LiDAR sensor is hitting obstacles.</p>

<p align="center">
<img width="934" height="632" alt="rvizmaps" src="https://github.com/user-attachments/assets/6036eeea-73ef-4281-8db9-f4a3261044d1" />
<img width="552" height="712" alt="foxglovemaps" src="https://github.com/user-attachments/assets/05ba50f4-b2ff-416f-b3a8-33a5c818d236" />
</p>

<p align="justify">More importantly, you will be able to visualize the Coordinate Frames (TF Tree): <code>base_footprint</code>, <code>odom</code>, and <code>map</code>.</p>

<p align="justify">The <code>base_footprint</code> frame is physically tied to the base of the robot (which is why you see the 3D robot model rendered there) and represents its current estimated pose. This estimated pose relies on the robot's internal odometry, which is why you see a connection from <code>base_footprint</code> to <code>odom</code>. The <code>odom</code> frame represents the exact point where the robot started moving, meaning it initially overlaps perfectly with <code>base_footprint</code>.</p>

<p align="justify">There is also a connection from <code>odom</code> to <code>map</code>, because our ultimate goal is to know the global pose of the robot. While the connection from <code>odom</code> to <code>base_footprint</code> only provides a local pose (where the robot is relative to where it turned on), the connection up to the <code>map</code> frame tells us where the robot is globally within the factory.</p>

<p align="justify">However, the core localization problem that <code>AMCL</code> solves is that this local odometry pose inevitably drifts over time due to accumulated wheel slip and measurement errors. We must continuously correct this drift by matching exteroceptive sensor readings (the LiDAR) with the known map to obtain an accurate, drift-free global pose.</p>

<p align="justify">When the <code>AMCL</code> node first launches, its default initial pose is set to the absolute center of the world. Because of this, you will see the robot spawn exactly in the center of the map in <code>RViz</code> and <code>Foxglove</code>, perfectly aligned with the map frame.</p>

<p align="justify">In reality, if you look at the <code>Gazebo</code> window, the robot does not spawn in the center of the factory; it spawns in a completely different location.</p>

<p align="justify">Once you start driving the robot, <code>AMCL</code> will attempt to correct this discrepancy by matching the LiDAR readings to the map architecture. This correction is mathematically reflected by shifting the odom frame (the robot's perceived starting point) within the map.</p>

<p align="justify">Because this automatic correction can take a long time to converge if the initial error is massive, it is highly recommended to use the <code>2D Pose Estimate</code> tool in <code>RViz</code>. Click the tool, then click and drag a green arrow on the map exactly where the robot is actually located in <code>Gazebo</code>. You will immediately see the robot model jump to that location. Suddenly, the blue LiDAR readings will align almost perfectly with the black walls of the map—you essentially just did the initial heavy lifting for the <code>AMCL</code> algorithm.</p>

<p align="justify">From there, teleoperate the robot around the factory. As the odometry changes, <code>AMCL</code> will use the movement and new LiDAR data to constantly refine the estimated pose. Eventually, you will see the <code>map</code> frame stationary at the center, connected to the <code>odom</code> frame (which now correctly sits where the robot spawned in <code>Gazebo</code>), and the <code>base_footprint</code> frame (the global pose) will perfectly track the robot's true position in <code>Gazebo</code>.</p>

<div align="center">
<video src="https://github.com/user-attachments/assets/05c31471-0b11-429a-98e8-355d5ca18e9f" controls="controls"></video>
</div>

<p align="justify">As a final detail, you will also see static transforms extending from the <code>map</code> to the specific locations of the ArUco markers on the walls. These act as external fixed references that can be utilized to further tune and refine the localization tasks.</p>

<p align="justify">This covers everything you need to know to operate the simulation. Explore the map, navigate to the trailer docking area to inspect the logos using the cameras, and try manipulating the pallets using the teleoperated forks—pick them up, transport them, and set them back down on the floor.</p>

<p align="center">
<img width="426" height="240" alt="manipulationpallets" src="https://github.com/user-attachments/assets/bc7de575-3ad7-47ad-b5b4-d72742d5eb9a" />
</p>

## Details

### Topic Naming Conventions

<p align="justify">
To guarantee that the code developed in the simulation translates seamlessly to the physical Puzzlebot, you must ensure that the sensor topics published by the robot's onboard Jetson match the following naming scheme.
</p>

> [!NOTE]
> These may differ from the official Manchester Robotics default configurations.

<ul>
  <li><i>Camera</i>: <code>/image_raw</code> (Type: <code>sensor_msgs/msg/Image</code>) and <code>/image_raw/compressed</code> (Type: <code>sensor_msgs/msg/CompressedImage</code>)</li>
  <li><i>LiDAR</i>: <code>/scan</code> (Type: <code>sensor_msgs/msg/LaserScan</code>)</li>
  <li><i>Odometry</i>: <code>/odom</code> (Type: <code>nav_msgs/msg/Odometry</code>)</li>
</ul>

<p align="justify">
The official <code>geometry_msgs/msg/Twist</code> command topic for the physical robot is <code>/cmd_vel</code>. This must remain unchanged.
</p>

<p align="justify">
Additionally, carefully review the <code>puzzlebot_bringup/launch/puzzlebot.launch.py</code> file, which initializes all the equivalent components for the physical robot just as <code>puzzlebot_bringup/launch/simulation_puzzlebot.launch.py</code> does for the simulation. Just ensure there is a dedicated node publishing odometry data somewhere in your real-world setup; the simulation lacks a standalone odometry node because <code>Gazebo</code> calculates and broadcasts it automatically. You can run the launch file for the real robot with the following command:
</p>

```bash
ros2 launch puzzlebot_bringup puzzlebot.launch.py
```

<p align="justify">
Or alternatively, use the alias:
</p>

```bash
puzzlebot
```

<p align="justify">
When adding new nodes, use the provided launch files as templates. Launch parameters such as <code>env_type</code> and <code>use_sim_time</code> are critical for the system to function correctly.
</p>

### The cmd_vel Pipeline

<p align="justify">
As mentioned, both the real and simulated Puzzlebot listen for kinematic commands on the <code>/cmd_vel</code> topic. This repository manages these velocity commands through a specific pipeline. Developers should adhere to this architecture to avoid conflicts when introducing new control elements (e.g., custom path planners or teleoperation GUIs).
</p>

<p align="justify">
It is highly recommended that any new control element publishes its commands as <code>geometry_msgs/msg/TwistStamped</code> messages, rather than standard <code>geometry_msgs/msg/Twist</code> messages (e.g., publishing to <code>/template/cmd_vel_stamped</code>). Alongside this element, you must launch a <code>twist_unstamper</code> node to convert the stamped message into a standard <code>geometry_msgs/msg/Twist</code> message. For example, the unstamper will output to <code>/template/cmd_vel</code>, which is then fed into the <code>twist_mux</code>.
</p>

<p align="justify">
The <code>twist_mux</code> node manages multiple control sources by assigning strict priorities and timeouts. This allows higher-priority sources (like a human operating a joystick) to safely override autonomous controllers, which might behave unpredictably. This node can also completely nullify all twist sources, which enables the software lock/unlock security feature described in the <i>First Steps</i> section, safely freezing the robot.
</p>

<p align="justify">
You can find a template for launching the unstamper node in <code>puzzlebot_control/launch/template_teleop.launch.py</code>. It is best practice to include this pipeline for any element controlling the robot. See <code>puzzlebot_control/launch/joystick_teleop.launch.py</code> for a practical example. Once the unstamper is configured, register the new unstamped topic inside the <code>puzzlebot_control/config/twist_mux.yaml</code> configuration file.
</p>

<p align="justify">
The rest of the pipeline operates automatically. Based on priority, <code>twist_mux</code> outputs the winning command to the <code>/cmd_vel_raw</code> topic. This command is then restamped by a <code>twist_stamper</code> node, outputting to <code>/cmd_vel_raw_stamped</code>. Next, the <code>puzzlebot_hardware/python_nodes/accel_limiter.py</code> node applies a slew-rate limit based on the maximum allowed linear and angular accelerations. This prevents sudden jerks, protects the motors from high current spikes, and ensures smooth physical motion by gradually stepping the current velocity toward the target velocity. 
</p>

<p align="justify">
The refined, smoothed output is then published directly to the final <code>/cmd_vel</code> topic recognized by the hardware and simulation. You can tune the maximum acceleration limits inside <code>puzzlebot_hardware/config/accel_limiter.yaml</code>, though the default values have been physically validated.
</p>

<img width="1918" height="709" alt="twistpipeline" src="https://github.com/user-attachments/assets/ad98c19c-2e66-4366-874e-d6de0edd336d" />

<p align="justify">
While it is technically possible to publish directly to <code>/cmd_vel</code>, doing so bypasses this entire architecture and is strongly discouraged. By skipping the pipeline, you lose critical safety features: emergency stop overrides, automatic prioritization of human teleoperation over autonomous code, and hardware protection against aggressive acceleration spikes.
</p>

### The Forklift Controller and Mux

<p align="justify">
The <code>puzzlebot_control/python_nodes/forklift_controller.py</code> node governs the forklift's movement within the simulation using an internal state machine. Its current state is continuously broadcast to the <code>Forklift Status</code> indicator on the <code>Foxglove</code> dashboard. You can configure physical limits, such as the maximum elevation (<code>max_z</code>), inside <code>puzzlebot_control/config/forklift_controller.yaml</code>.
</p>

<p align="justify">
Mirroring the <code>twist_mux</code> architecture, this controller implements a custom <code>forklift_mux</code>, configurable via <code>puzzlebot_control/config/forklift_mux.yaml</code>. This handles source prioritization, timeouts, and the software lock/unlock safety feature.
</p>

<p align="justify">
The controller dynamically infers message types based on the YAML dictionary key (the source designation) assigned in the configuration file, not the actual <code>ROS</code> topic path it subscribes to. For example, in the configuration block below, if the source key contains the word <code>joy</code> (e.g., <code>joystick</code>), it expects a <code>sensor_msgs/msg/Joy</code> message. If the key contains <code>twist</code> (e.g., <code>foxglove_twist</code>), it expects a <code>geometry_msgs/msg/Twist</code> message. Any other naming convention without these keywords (e.g., <code>template</code>) defaults to expecting a <code>std_msgs/msg/Float64</code> message.
</p>

```yaml
forklift_controller:
  ros__parameters:
    locks:
      e_stop:
        topic: ~/lock
        timeout: 0.0    
        priority: 90   

    topics:
      joystick:
        topic: /joy
        timeout: 0.2
        priority: 255
      foxglove_twist:
        topic: ~/foxglove/target
        timeout: 0.2
        priority: 100
      template:
        topic: ~/template/target
        timeout: 0.0
        priority: 90
```

<p align="justify">
Fork elevation targets are normalized between <code>0.0</code> and <code>1.0</code>. Sending a <code>1.0</code> commands the forks to reach the absolute <code>max_z</code> height, <code>0.5</code> commands them to the halfway point, and <code>0.0</code> returns them to the lowest possible resting position.
</p>

<p align="justify">
You can register as many <code>Joy</code>, <code>Twist</code>, or <code>Float64</code> sources as needed in the <code>forklift_mux.yaml</code> file. The <code>Float64</code> interface is explicitly designed for sending autonomous target commands rather than continuous teleoperation. For example, to send an autonomous command:
</p>

```bash
ros2 topic pub --once /forklift_controller/template/target std_msgs/msg/Float64 "{data: 0.5}"
```

<p align="justify">
This action will trigger state changes visible on the <code>Foxglove Forklift Status</code> panel. The available states are:
</p>

<ul>
  <li><i>IDLE</i>: Not receiving any command.</li>
  <li><i>RUNNING_[ACTIVE_SOURCE]</i>: Where <code>[ACTIVE_SOURCE]</code> dynamically reflects the name of the active input (e.g., <code>RUNNING_JOYSTICK</code> for a <code>joystick</code> (<code>Joy</code>) command, <code>RUNNING_FOXGLOVE_TWIST</code> for a <code>foxglove_twist</code> (<code>Twist</code>) command, or <code>RUNNING_TEMPLATE</code> for a <code>template</code> (<code>Float64</code>) command).</li>
  <li><i>REACHED</i>: Triggered once a <code>Float64</code> target height is successfully attained. This flag is critical for autonomous logic, as continuous teleoperation does not require an explicit "target reached" acknowledgment.</li>
  <li><i>LOCKED</i>: The forks are frozen and will not move until an explicit unlock command is received.</li>
  <li><i>DISABLED</i>: The controller node has been completely deactivated.</li>
</ul>

<p align="justify">
To monitor the current operational state of the forklift controller directly from your terminal, you can echo its status topic using the following command:
</p>

```bash
ros2 topic echo /forklift_controller/status
```

<p align="justify">
This modular controller architecture was designed to be platform-agnostic, making it easily adaptable to different physical forklift designs or mechanisms.
</p>

<p align="justify">
Finally, to read the real-time normalized height of the forks during simulation, you must listen to the <code>/joint_states</code> topic, extract the position value for <code>forks_joint</code>, and divide it by your configured <code>max_z</code>. You can retrieve the raw joint value using the following command, and then manually divide the output by the <code>max_z</code> value specified in your configuration file:
</p>

```bash
ros2 topic echo --once /joint_states | awk '
/^name:/ { in_name=1; in_pos=0; idx=0; target=-1; next }
in_name && /^- / { if ($2 == "forks_joint") target=idx; idx++; next }
/^position:/ { in_name=0; in_pos=1; idx=0; next }
in_pos && /^- / { if (idx == target) { print $2; exit }; idx++; next }
'
```

### Foxglove Configuration

<p align="justify">
As mentioned in the <i>First Steps</i> section, you can modify the default <code>WebSocket</code> host address and port, along with other performance-tuning parameters for the <code>ROS 2</code> to <code>Foxglove</code> bridge. These settings can be adjusted inside the <code>puzzlebot_bringup/config/foxglove_bridge.yaml</code> configuration file.
</p>

<p align="justify">
Additionally, the custom dashboard layout imported into the <code>Foxglove Studio</code> application is located at <code>puzzlebot_bringup/foxglove_config/display_foxglove.json</code>. If you make modifications or add new visualization panels to your <code>Foxglove</code> workspace during development, you can export and overwrite this <code>JSON</code> file to permanently save your new layout.
</p>

### Teleoperation Customization and Kinematic Limits

<p align="justify">
As mentioned in the <i>First Steps</i> section, if you need to fix or customize the joystick mappings, you can do so by editing the <code>puzzlebot_control/config/joystick_teleop.yaml</code> file. Here, you can modify the axis assignments and the scale modifiers to adjust the maximum linear X and angular Z twist speeds sent by the controller.
</p>

<p align="justify">
However, for the <code>Gazebo</code> simulation, these teleoperation commands are ultimately clamped by the strict kinematic limits defined in <code>puzzlebot_control/config/simulation_controller.yaml</code>. This configuration dictates the absolute maximum velocities and accelerations for the robot to simulate realistic physics. Notably, these limits mirror those used by the <code>puzzlebot_hardware/python_nodes/accel_limiter.py</code> node.
</p>

<p align="justify">
Beyond just velocity limits, the <code>simulation_controller.yaml</code> file is the backbone of the simulated robot's movement. It configures the <code>diff_drive_controller</code> (which actively calculates and broadcasts the simulation's odometry from the <code>odom</code> to the <code>base_footprint</code> frame), the <code>joint_state_broadcaster</code>, and the <code>forks_controller</code>. Note that this <code>forks_controller</code> is a low-level joint velocity controller for the <code>Gazebo</code> physics engine, which should not be confused with the high-level <code>Python</code> state machine that manages target heights. All of these low-level controllers are initialized via the <code>puzzlebot_control/launch/simulation_controller.launch.py</code> file.
</p>

### Robot Description (URDF, Gazebo & ROS 2 Control)

<p align="justify">
The aforementioned controllers are tightly coupled to the robot's physical description files located in the <code>puzzlebot_description/urdf/</code> directory. To maintain a clean and modular architecture, the robot's model is split into three specific <code>Xacro</code> files:
</p>

<ul>
  <li><i><code>puzzlebot_description/urdf/puzzlebot.urdf.xacro</code></i>: The core structural file. It defines the robot's kinematics, meshes, inertias, collision geometries, and joints (including the continuous wheel joints and the prismatic forks joint).</li>
  <li><i><code>puzzlebot_description/urdf/puzzlebot_gazebo.xacro</code></i>: Contains all Gazebo-specific physics overrides (like friction coefficients) and sensor plugins. Here, you can modify the parameters of the simulated GPU LiDAR, the primary camera, and the debug forks camera. (Note: These are already pre-tuned to closely match the real Puzzlebot hardware).</li>
  <li><i><code>puzzlebot_description/urdf/puzzlebot_ros2_control.xacro</code></i>: The bridge between the <code>URDF</code> and the <code>ROS 2 Control</code> framework. It loads the <code>gz_ros2_control</code> hardware plugin and links the joints to the configurations defined in <code>simulation_controller.yaml</code>.</li>
</ul>

<p align="justify">
If you need to inspect, modify, or visualize the <code>URDF</code> model in <code>RViz</code> without booting up the heavy <code>Gazebo</code> simulation engine, run the following command:
</p>

```bash
ros2 launch puzzlebot_description display_rviz.launch.py
```

<p align="justify">
Or alternatively, use the alias:
</p>

```bash
display_rviz
```

<p align="justify">
The 3D assets for the robot's physical description are located inside the <code>puzzlebot_description/meshes</code> directory.
</p>

### Modifying the RoboArena 4.0 World

<p align="justify">
The digital twin of the factory floor is defined in the <code>puzzlebot_description/worlds/e80_factory.sdf</code> file. If you want to modify the environment—such as adding a new pallet/ArUco, or changing QR/ArUco textures—you can do so here. Custom image textures for the environment are stored in the <code>puzzlebot_description/materials/textures</code> directory.
</p>

<p align="justify">
To test world modifications quickly by launching only the <code>Gazebo</code> simulation, run:
</p>

```bash
ros2 launch puzzlebot_description simulation_gazebo.launch.py
```

<p align="justify">
Or alternatively, use the alias:
</p>

```bash
simulation_gazebo
```

<p align="justify">
To control the actual physical spawn pose of the robot within the Gazebo simulation (which, as you may recall, differs from the default initial pose estimated by <code>Nav2 AMCL</code>), you must modify the <code>puzzlebot_description/launch/simulation_gazebo.launch.py</code> file
</p>

```python
gz_spawn_entity_node = Node(
    package='ros_gz_sim',
    executable='create',
    arguments=[
        '-topic', 'robot_description',
        '-name', 'puzzlebot',
        '-x', '-1.8',
        '-y', '0.0',
        '-z', '0.0',
        '-Y', '-1.57'
    ],
    output='screen'
)
```

<p align="justify">
Finally, any default configurations for the <code>RViz</code> interfaces used in the <code>puzzlebot_description/launch/display_rviz.launch.py</code>, <code>puzzlebot_bringup/launch/simulation_puzzlebot.launch.py</code>, and <code>puzzlebot_bringup/launch/puzzlebot.launch.py</code> launch files can be found and modified inside the <code>puzzlebot_description/rviz_config/</code> directory.
</p>

### Nav2 and Mapping

<p align="justify">
The <code>puzzlebot_navigation/launch/nav2.launch.py</code> file initializes the core navigation components: the <code>Nav2 Map Server</code>, <code>Costmap</code>, and <code>AMCL</code> nodes. You can fine-tune the configuration parameters for the <code>Costmap</code> and <code>AMCL</code> inside the <code>puzzlebot_navigation/config/nav2.yaml</code> file. For instance, this is where you can modify the default initial pose for the <code>AMCL</code> algorithm:
</p>

```yaml
set_initial_pose: true
initial_pose:
  x: 0.0
  y: 0.0
  z: 0.0
  yaw: 0.0
```

<p align="justify">
Inside the <code>puzzlebot_navigation/maps/</code> directory, you will find the pre-mapped layouts of the factory (both real and simulated). These static maps are provided in the standard <code>ROS 2</code> mapping format: a <code>.pgm</code> image file representing the occupancy grid and its corresponding <code>.yaml</code> metadata file.
</p>

<p align="justify">
The simulation launch file (<code>puzzlebot_bringup/launch/simulation_puzzlebot.launch.py</code>) streams the <code>simulation_e80_factory.pgm</code> map to the <code>/map</code> topic, whereas the launch file for the real robot (<code>puzzlebot_bringup/launch/puzzlebot.launch.py</code>) streams the <code>e80_factory.pgm</code> map.
</p>

<p align="justify">
Additionally, the <code>puzzlebot_navigation/config/simulation/fixed_arucos_poses.json</code> file is used to store the exact coordinates of the ArUco markers placed throughout the <code>Gazebo</code> factory world. These positions are read by the <code>puzzlebot_navigation/python_nodes/fixed_aruco_pose_streamer.py</code> node, which continuously broadcasts them as static transforms (e.g., map → aruco_X) directly into the ROS 2 TF tree to serve as external references for localization.
</p>

### Dynamic Configuration Fallback

<p align="justify">
You might have noticed that the <code>puzzlebot_navigation/config/</code> directory contains <code>simulation/</code> and <code>real/</code> subfolders, each housing its own <code>fixed_arucos_poses.json</code> file. This separation exists because the physical ArUco marker poses differ slightly from their simulated counterparts and are subject to future physical adjustments.
</p>

<p align="justify">
This dynamic configuration loading applies across all packages. If a configuration needs to be tuned differently for the physical robot versus the digital twin (for instance, a <code>nav2.yaml</code> file), you can simply place the environment-specific versions inside the respective <code>config/simulation/</code> or <code>config/real/</code> directories. The launch files are programmed to automatically detect the current environment and load the correct file. Conversely, if a configuration is universal and works for both setups, it can remain directly inside the base <code>config/</code> directory to act as a shared fallback.
</p>

<p align="justify">
Here is a hypothetical example of how this directory structure could look in practice. Please note that while the configuration files shown below belong to different packages in the actual repository, they are grouped together here simply to illustrate the fallback logic:
</p>

```text
config/
├── real/
│   ├── fixed_arucos_poses.json      # Specific to the physical robot
│   └── nav2.yaml                    # Specific to the physical robot
├── simulation/
│   ├── fixed_arucos_poses.json      # Specific to the digital twin
│   └── nav2.yaml                    # Specific to the digital twin
├── accel_limiter.yaml               # Universal (Fallback for both)
├── joystick_teleop.yaml             # Universal (Fallback for both)
└── twist_mux.yaml                   # Universal (Fallback for both)
```

<p align="justify">
For this reason, the <code>env_type</code> and <code>use_sim_time</code> launch parameters—as previously highlighted in the <i>Topic Naming Conventions</i> section—are absolutely critical for the system to function correctly and load the appropriate configuration files.
</p>

### Utility Scripts

<p align="justify">
Finally, inside the <code>puzzlebot-sim/scripts</code> directory, you will find several utility scripts designed to simplify common development, simulation, and data-processing tasks:
</p>

<p align="justify">
The <code>puzzlebot-sim/scripts/compute_inertias.py</code> utility automatically computes the mass and principal inertia components of the robot's STL meshes using <code>trimesh</code>. The script searches the robot description's  <code>puzzlebot_description/models</code> and <code>puzzlebot_description/meshes</code> directories, determines the mass from the configured material density, and generates the corresponding inertial parameters. The resulting values are written to <code>puzzlebot_description/inertias_urdf.txt</code>.
</p>

<p align="justify">
Run it from the repository root with:
</p>

```bash
python3 scripts/compute_inertias.py
```

<p align="justify">
The <code>puzzlebot-sim/scripts/bag_to_jpg.py</code> script extracts camera frames from a <code>ROS 2</code> bag and saves them as <code>.jpg</code> images. It supports both standard <code>sensor_msgs/msg/Image</code> and compressed <code>sensor_msgs/msg/CompressedImage</code> topics, automatically handling the corresponding image conversion. The script also allows you to control the extraction rate by skipping a configurable number of frames, which is useful when generating image datasets without saving every frame recorded in the bag.
</p>

<p align="justify">
For example:
</p>

```bash
python3 scripts/bag_to_jpg.py <bag_path> \
    --output dataset_frames \
    --topic /image_raw \
    --skip 5
```

<p align="justify">
By default, the script extracts one frame every five messages from <code>/image_raw</code> and stores the resulting images in the <code>dataset_frames</code> directory.
</p>

<p align="justify">
The extracted images were used to generate a dataset from the RoboArena 4.0 simulation, specifically containing images of the client logos displayed on the simulated trailers. This dataset was subsequently used to train a <code>YOLO</code> object-detection model, enabling the perception system to automatically identify and classify the client logos during autonomous navigation.
</p>

<p align="justify">
The <code>puzzlebot-sim/scripts/qr_generator.py</code> script generates the QR-code textures used by the simulated pallets. The current configuration creates QR codes containing the client identifiers used by the RoboArena 4.0 scenario:
</p>

```text
Emezon
Wolmar
Popsi
```

<p align="justify">
Each QR code is saved as a <code>PNG</code> texture inside <code>puzzlebot_description/materials/textures</code>. These textures can then be assigned to the corresponding pallet models in the Gazebo environment, allowing the perception and autonomous-navigation pipeline to identify the intended client from the pallet's QR code.
</p>

<p align="justify">
Run the script from the repository root:
</p>

```bash
python3 scripts/qr_generator.py
```
