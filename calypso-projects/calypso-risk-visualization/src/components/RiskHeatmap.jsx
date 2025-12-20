import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import './RiskHeatmap.css';

const RiskHeatmap = ({ data, onDrillDown }) => {
  const svgRef = useRef();
  const margin = { top: 50, right: 50, bottom: 100, left: 100 };
  const width = 800 - margin.left - margin.right;
  const height = 600 - margin.top - margin.bottom;

  useEffect(() => {
    if (!data || data.length === 0) return;

    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();

    const g = svg.append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // Extract unique books and instruments
    const books = [...new Set(data.map(d => d.book))];
    const instruments = [...new Set(data.map(d => d.instrument))];

    // Create scales
    const xScale = d3.scaleBand()
      .domain(instruments)
      .range([0, width])
      .padding(0.1);

    const yScale = d3.scaleBand()
      .domain(books)
      .range([0, height])
      .padding(0.1);

    const colorScale = d3.scaleSequential(d3.interpolateRdYlGn)
      .domain([d3.max(data, d => d.riskValue), d3.min(data, d => d.riskValue)]);

    // Create rectangles
    const cells = g.selectAll('.cell')
      .data(data)
      .enter()
      .append('rect')
      .attr('class', 'cell')
      .attr('x', d => xScale(d.instrument))
      .attr('y', d => yScale(d.book))
      .attr('width', xScale.bandwidth())
      .attr('height', yScale.bandwidth())
      .attr('fill', d => colorScale(d.riskValue))
      .attr('stroke', '#fff')
      .on('click', (event, d) => {
        if (onDrillDown) {
          onDrillDown(d);
        }
      })
      .on('mouseover', function(event, d) {
        d3.select(this).attr('stroke-width', 3);
        
        const tooltip = d3.select('body').append('div')
          .attr('class', 'risk-tooltip')
          .style('opacity', 0);

        tooltip.transition()
          .duration(200)
          .style('opacity', .9);

        tooltip.html(`
          <strong>${d.book} - ${d.instrument}</strong><br/>
          Risk Value: ${d.riskValue.toFixed(2)}<br/>
          Delta: ${d.delta || 0}<br/>
          Gamma: ${d.gamma || 0}<br/>
          Vega: ${d.vega || 0}
        `)
          .style('left', (event.pageX + 10) + 'px')
          .style('top', (event.pageY - 10) + 'px');
      })
      .on('mouseout', function() {
        d3.select(this).attr('stroke-width', 1);
        d3.selectAll('.risk-tooltip').remove();
      });

    // Add axes
    g.append('g')
      .attr('transform', `translate(0,${height})`)
      .call(d3.axisBottom(xScale)))
      .selectAll('text')
      .attr('transform', 'rotate(-45)')
      .style('text-anchor', 'end');

    g.append('g')
      .call(d3.axisLeft(yScale));

    // Add labels
    svg.append('text')
      .attr('transform', 'rotate(-90)')
      .attr('y', 20)
      .attr('x', -height / 2)
      .style('text-anchor', 'middle')
      .text('Book');

    svg.append('text')
      .attr('x', width / 2)
      .attr('y', height + margin.bottom - 20)
      .style('text-anchor', 'middle')
      .text('Instrument');
  }, [data, margin, width, height, onDrillDown]);

  return (
    <div className="risk-heatmap">
      <h3>Risk Heatmap</h3>
      <svg ref={svgRef} width={800} height={600}></svg>
    </div>
  );
};

export default RiskHeatmap;



