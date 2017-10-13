$.getJSON("/getInteractions", function (data) {
    var cy = cytoscape({
        container: document.getElementById('graph-div'),
        elements: data,

        style: [ // the stylesheet for the graph
            {
                selector: 'node',
                style: {
                    'background-color': '#666',
                    'label': 'data(name)'
                }
            },

            {
                selector: 'edge',
                style: {
                    'width': 3,
                    'line-color': '#ccc',
                    'target-arrow-color': '#ccc',
                    'target-arrow-shape': 'triangle',
                    'label': 'data(type)'
                }
            }
        ],

        layout: {
            name: 'grid',
            rows: 5,
            cols: 10
        }
    });
});
