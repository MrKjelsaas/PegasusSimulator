# Python garbage collenction and asyncronous API
import gc
import asyncio

# External packages
import numpy as np

# Omniverse general API
import carb
import omni.ext
import omni.ui as ui

# Isaac Speficic extensions API
from omni.isaac.core import World
from omni.isaac.core.utils.viewports import set_camera_view
from omni.isaac.core.utils.stage import create_new_stage_async, set_stage_up_axis, clear_stage, add_reference_to_stage, get_current_stage

# Pegasus Extension Files
from pegasus_isaac.utils import createObject
from pegasus_isaac.params import EXTENSION_NAME, ROBOTS, DEFAULT_WORLD_SETTINGS

# TODO - remove this - only for debugging purposes
from omni.isaac.core.utils.nucleus import get_assets_root_path

# Quadrotor vehicle
from pegasus_isaac.logic.quadrotor import Quadrotor

import omni.physx

# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class Pegasus_isaacExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    def on_startup(self, ext_id):
        
        carb.log_info("Pegasus Isaac extension startup")

        # Save the extension id
        self._ext_id = ext_id
        
        # Basic world configurations
        self._world_settings = DEFAULT_WORLD_SETTINGS
        self._world: World = World(**self._world_settings)

        # Build the extension UI
        self.build_ui()

    def build_ui(self):
        """
        Method that builds the actual extension UI
        """
        
        carb.log_info("Pegasus Isaac extension UI startup")
        
        # Create the widget window
        self._window: ui.Window = ui.Window(
            title=EXTENSION_NAME,
            width=0.0,
            height=0.0,
            visible=True)
        
        # Method to check whether the visibility of the extension widget has changed 
        self._window.set_visibility_changed_fn(self.on_shutdown)
   
        # Define the UI of the widget window
        with self._window.frame:
            
            # Vertical Stack of menus
            with ui.VStack():
                
                # Label for the buttons in the UI
                label = ui.Label("Simulation Setup")
                
                # Button to load the world into the stage
                load_button = ui.Button("Load", clicked_fn=self.load_button_callback)
                
                # Button to reset the stage
                reset_button = ui.Button("Reset", clicked_fn=self.reset_button_callback)
                
                # Button to load the drone
                drone_button = ui.Button("Drone", clicked_fn=self.load_drone_callback)
                
                # Button to set the camera view
                camera_button = ui.Button("Set Camera", clicked_fn=self.set_camera_callback)
                
                # Button do adjust the physics timestep
                physics_button = ui.Button("Set Physics", clicked_fn=self.set_physics_callback)

                #
                test_button = ui.Button("do nothing", clicked_fn=lambda : print("test"))
                
    def load_button_callback(self):
        """
        Callback function that is called when the load button of the extension is pressed
        """
        carb.log_info("Pressed the load button")
        
        # Load a world into the stage
        asyncio.ensure_future(self.load_world_async())

    def reset_button_callback(self):
        """
        Callback function that is called when the reset button of the extension is pressed
        """
        carb.log_info("Pressed the reset button")
        
        # Reset the world in the stage
        self.clear_world()
        
    def load_drone_callback(self):
        """
        Callback function that is called when the load drone button of the extension is pressed
        """
        carb.log_info("Pressed the load drone button")
        
        # Check if we have a world already. If not, just return
        #if self._world is None:
        #    carb.log_warn("No world object yet. Drone not spawned")
        #    return
        
        nucleus_server = get_assets_root_path()
        asset_path = nucleus_server + "/Isaac/Props/Blocks/nvidia_cube.usd"

        asset_path = ROBOTS["Quadrotor"]
        
        from pxr import Gf
        self.prims = []
        position = Gf.Vec3d(0, 0, 1.0)
        """
        self.prims = createObject(
            '/World/iris', 
            get_current_stage(), 
            asset_path, 
            False, 
            position=position, 
            group=self.prims, 
            density=1, 
            scale=Gf.Vec3d(1, 1, 1)
        )
        """

        #prim = add_reference_to_stage(usd_path=ROBOTS["Quadrotor"], prim_path="/World/quadrotor")

        #self._world.scene.add(Robot())
        
        #from omni.isaac.core.prims import XFormPrim
        #self._world.scene.add(XFormPrim("/World/quadrotor", visible=True, translation=[0.0, 0.0, 1.0]))
        #carb.log_warn(type(prim))

        #prim_path = omni.usd.get_stage_next_free_path(get_current_stage(), "/World/quadrotor", False)
        #prim = add_reference_to_stage(usd_path=ROBOTS["Quadrotor"], prim_path=prim_path)
        #self._world.scene.add(prim)

        
        #self._world.scene.add(prim)

        # Create a new primitive in the stage
        #self.prim = self._world.stage.DefinePrim("/World/quadrotor", "Xform")
        #self.prim.GetReferences().AddReference(ROBOTS["Quadrotor"])
        
        #self.prim = self._world.stage.DefinePrim("/World/quadrotor2", "Xform")
        #self.prim.GetReferences().AddReference(ROBOTS["Quadrotor"])

        # Bind that primitive to the content of the USD file

        #carb.log_warn("Test 2")

        quad = Quadrotor("/World/quadrotor", ROBOTS["Quadrotor"], self._world)


        # Add the callbacks to
        #self._world.add_physics_callback("/World/quadrotor", self.physics_callback)

        #dc = _dynamic_control.acquire_dynamic_control_interface()
        # Check to see what type of object the target prim is
        #obj_type = dc.peek_object_type("/World/quadrotor")

        
        #carb.log_warn(obj_type)
        
    def physics_callback(self, dt):
        """
        Callback to update the physics of the drone
        """
        carb.log_warn("Running physics: " + str(dt))
        #carb.log_warn(self.prims[-1])
        #carb.log_warn("/updat")
        
    def set_camera_callback(self):
        """
        Callback function that is called whent the load camera button of the extension is pressed
        """
        carb.log_info("Pressed the set camera button")
        
        # Set the camera view to a fixed value
        set_camera_view(eye=np.array([5, 5, 5]), target=np.array([0, 0, 0]))
             
    def set_physics_callback(self):
        """
        Callback that sets the physics parameters for the simulation
        """
        carb.log_info("Pressed the set physics button")
        
        # Set the timestep update for the physics solver
        self._world.set_simulation_dt(1.0 / 250.0)         
    
    async def load_world_async(self):
        """
        Function called when clicking the load World button
        """

        # Create a new empty stage
        await create_new_stage_async()

        # Make sure that we use Z as the up axis
        set_stage_up_axis('z')

        # Create a new empty with the correct settings and initialize it
        self._world = World(**self._world_settings)
        await self._world.initialize_simulation_context_async()

        # Reset and pause the world simulation
        await self._world.reset_async()
        await self._world.pause_async()
        
        # Load a ground in the world
        self._world.scene.add_default_ground_plane()
        
    def clear_world(self):
        
        # Clear the Robot object wrapper
        self.robot = None
        
        # Clear the world
        self._world.clear()

        # Clear the stage
        clear_stage()
        
        # Cleanup the world pointer
        self._world = None
        
        # Cleanup the primitives list
        self.prims = []

        # Call python's garbage collection
        gc.collect()
        
                    
    def set_world_settings(self, physics_dt=None, stage_units_in_meters=None, rendering_dt=None):
        """
        Set the current world settings to the pre-defined settings
        """

        # Set the physics engine update rate
        if physics_dt is not None:
            self._world_settings["physics_dt"] = physics_dt

        # Set the units of the simulator to meters
        if stage_units_in_meters is not None:
            self._world_settings["stage_units_in_meters"] = stage_units_in_meters

        # Set the render engine update rate (might not be the same as the physics engine)
        if rendering_dt is not None:
            self._world_settings["rendering_dt"] = rendering_dt

    def on_shutdown(self):
        """
        Callback called when the extension is shutdown
        """
        print("Pegasus Isaac extension shutdown")
        
        self.clear_world()