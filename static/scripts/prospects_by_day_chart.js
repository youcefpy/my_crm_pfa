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
  'Prospects a traité'
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
  lostProspectsByAgentLabel,
  lostProspectsByAgentData,
  'bar',
  'Prospects Perdus par agent'
);

//Prospet perdu par source
renderChart(
  'topPerformingAgentsChart',
  lostLeadBySourceLabel,
  lostLeadBySourceData,
  'pie',
  'Prospet perdu par source'
);


// total leads (plus loss)
renderChart(
  'totalLeadsChart',
  totalLeadsLabels,
  totalLeadsData,
  'bar',
  'Total des prospet par jour'
);