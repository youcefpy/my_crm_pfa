let chartInstance;

// Chart Configurations
const chartConfigs = {
    prospectsByDay: {
        labels: chartLabels,
        data: chartData,
        type: 'bar',
        label: 'Prospects par Jour'
    },
    clientsByMonthChart: {
        labels: leadsByMonthlabel,
        data: leadsByMonthData,
        type: 'bar',
        label: 'Prospet Par Mois'
    },
    agentsComparisonChart: {
        labels: agentsComparisonLabels,
        data: agentsComparisonData,
        type: 'bar',
        label: 'Clients par Agent'
    },
    prospectsBySourceChart: {
        labels: prospectsBySourceLables,
        data: prospectsBySourceData,
        type: 'pie',
        label: 'Répartition des Prospects par Source'
    },
    lostProspectsBySourceChart: {
        labels: lostProspectsByAgentLabel,
        data: lostProspectsByAgentData,
        type: 'bar',
        label: 'Prospects Perdus par Agent'
    },
    topPerformingAgentsChart: {
        labels: lostLeadBySourceLabel,
        data: lostLeadBySourceData,
        type: 'pie',
        label: 'Prospet Perdus par Source'
    },
    totalLeadsChart: {
        labels: totalLeadsLabels,
        data: totalLeadsData,
        type: 'bar',
        label: 'Total des Prospects par Jour'
    }
};

//fonction pour changer le graphe dans le canva
function renderChart(chartId) {
    const chartConfig = chartConfigs[chartId];
    const ctx = document.getElementById('dynamicChartCanvas').getContext('2d');

    // distruction du graphe
    if (chartInstance) {
        chartInstance.destroy();
    }

    //creation de graphe
    chartInstance = new Chart(ctx, {
        type: chartConfig.type,
        data: {
            labels: chartConfig.labels,
            datasets: [{
                label: chartConfig.label,
                data: chartConfig.data,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: chartConfig.type === 'pie' ? {} : {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

//selection de la classe avec le nom switch-chart
document.querySelectorAll('.switch-chart').forEach(button => {
    button.addEventListener('click', () => {
        //recuperer l'attribut de data-chart
        const chartId = button.getAttribute('data-chart');
        
        document.querySelectorAll('.switch-chart').forEach(btn => {
          btn.classList.remove('btn-primary');
          btn.classList.add('btn-secondary');
      });
      button.classList.remove('btn-secondary');
      button.classList.add('btn-primary');

        // Render the selected chart
        renderChart(chartId);
    });
});

// graphe par defaut
const defaultChartId = 'prospectsByDay';
renderChart(defaultChartId);

// Set the default active button
document.querySelector(`[data-chart="${defaultChartId}"]`).classList.add('btn-primary');
document.querySelector(`[data-chart="${defaultChartId}"]`).classList.remove('btn-secondary');