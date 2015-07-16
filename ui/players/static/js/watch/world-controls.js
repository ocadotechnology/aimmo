// World Manipulation
const CONTROLS = Object.create(
    {
        world : null,
        viewer : null,

        init : function(world, viewer) {
            this.world = world;
            this.viewer = viewer;
        },

        initialiseWorld : function(width, height, worldLayout) {
            this.world.width = width;
            this.world.height = height;
            this.world.layout = worldLayout;

            this.viewer.reDrawWorldLayout();
        },
        setState : function(players, items) {
            this.world.players = players;
            this.world.items = items;

            this.viewer.reDrawState();
        }
    }
);