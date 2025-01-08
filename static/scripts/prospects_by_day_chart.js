function renderChart(ctxId, labels, data, chartType, label) {
  const ctx = document.getElementById(ctxId);
  new Chart(ctx, {
      type: chartType,
      data: {
          labels: labels,
          datasets: [{
              label: label,
              data: data,
              borderWidth: 1
          }]
      },
      options: {
          scales: {
              y: {
                  beginAtZero: true
              }
          }
      }
  });
}

// Répartition des Prospects par jour
renderChart(
  'prospectsByDay',
  chartLabels,
  chartData,
  'bar',
  'Prospects par Source'
);


// Répartition des Prospects par Source
renderChart(
  'prospectsBySourceChart',
  prospectsBySourceLables,
  prospectsBySourceData,
  'pie',
  'Prospects par Source'
);

// Comparaison des Agents
renderChart(
  'agentsComparisonChart',
  agentsComparisonLabels,
  agentsComparisonData,
  'bar',
  'Clients par Agent'
);

// Clients Gagnés par Mois
renderChart(
  'clientsByMonthChart',
  leadsByMonthlabel,
  leadsByMonthData,
  'bar',
  'Prospet Par Mois'
);

// Prospects Perdus par Source
renderChart(
  'lostProspectsBySourceChart',
  lostProspectsBySourceLabel,
  lostProspectsBySourceData,
  'pie',
  'Prospects Perdus'
);

// Agents les Plus Performants
renderChart(
  'topPerformingAgentsChart',
  topPerformingAgentslabel,
  topPerformingAgentsData,
  'bar',
  'Agents les Plus Performants'
);
