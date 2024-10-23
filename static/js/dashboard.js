document.addEventListener('DOMContentLoaded', function () {
    const plotButton = document.getElementById('plot-graph');
    const multiAttributeGraph = document.getElementById('multi-attribute-graph');
    const singleGraphsContainer = document.getElementById('single-graphs-container');
    const multiGraphContainer = document.getElementById('multi-graph-container');
    const attributesCheckboxes = document.getElementById('attributes-checkboxes');
    
    let attributes = [];
    let dataset = [];

    // Fetch dataset and columns from the server
    fetch('/get_data')
        .then(response => response.json())
        .then(data => {
            dataset = data;
            if (dataset.length > 0) {
                attributes = Object.keys(dataset[0]);
                initializeUI();
                plotAllSingleAttributeGraphs();
            }
        })
        .catch(error => console.error('Error fetching data:', error));

    function initializeUI() {
        // Dynamically generate checkboxes for each attribute
        attributes.forEach(attr => {
            const checkboxDiv = document.createElement('div');
            checkboxDiv.classList.add('form-check');
            checkboxDiv.innerHTML = `
                <input class="form-check-input" type="checkbox" value="${attr}" id="${attr}">
                <label class="form-check-label" for="${attr}">
                    ${attr}
                </label>
            `;
            attributesCheckboxes.appendChild(checkboxDiv);
        });
    }

    plotButton.addEventListener('click', () => {
        const selectedMultiGraph = multiAttributeGraph.value;
        const selectedAttributes = Array.from(attributesCheckboxes.querySelectorAll('input[type="checkbox"]:checked'))
            .map(checkbox => checkbox.value);

        // Clear previous multi-attribute graph
        multiGraphContainer.innerHTML = '';

        if (selectedMultiGraph && selectedAttributes.length) {
            // Plot multi-attribute graph
            plotMultiAttributeGraph(selectedMultiGraph, selectedAttributes);
        }
    });

    function plotAllSingleAttributeGraphs() {
        attributes.forEach(attribute => {
            const graphTypes = ['histogram', 'boxplot', 'pie']; // List of single attribute graph types
            graphTypes.forEach(type => {
                plotSingleAttributeGraph(type, attribute);
            });
        });
    }

    function plotSingleAttributeGraph(graphType, attribute) {
        // Implement graph plotting logic based on graphType and attribute
        // Use dataset to plot the graph
        const graphDiv = document.createElement('div');
        graphDiv.classList.add('mb-4');
        graphDiv.textContent = `Plotting ${graphType} for ${attribute}`;
        singleGraphsContainer.appendChild(graphDiv);
        // Here you can add actual graph rendering using libraries like Plotly, Chart.js, etc.
    }

    function plotMultiAttributeGraph(graphType, attributes) {
        // Implement graph plotting logic based on graphType and attributes
        // Use dataset to plot the graph
        const graphDiv = document.createElement('div');
        graphDiv.classList.add('mb-4');
        graphDiv.textContent = `Plotting ${graphType} for ${attributes.join(', ')}`;
        multiGraphContainer.appendChild(graphDiv);
        // Here you can add actual graph rendering using libraries like Plotly, Chart.js, etc.
    }
});
