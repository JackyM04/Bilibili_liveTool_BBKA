import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import './index.css'
function ChartComponent() {
  const chartRef = useRef(null);

  useEffect(() => {
    const fetchDataAndDrawChart = () => {
      fetch('http://127.0.0.1:12310/get_chart_data/')
          .then(response => {
              if (!response.ok) {
                  throw new Error('Network response was not ok');
              }
              return response.json();
          })
          .then(data => {
              d3.select(chartRef.current).html("");
              drawChart(data.labels, data.counts);
          })
          .catch(error => {
              console.log('Fetch error:', error);
          });
    }

    fetchDataAndDrawChart();

    const intervalId = setInterval(fetchDataAndDrawChart, 1000);

    window.addEventListener('resize', fetchDataAndDrawChart);

    return () => {
      clearInterval(intervalId);
      window.removeEventListener('resize', fetchDataAndDrawChart);
    };
  }, []);

  const drawChart = (labels, counts) => {
    const width = document.documentElement.clientWidth;
    const height = document.documentElement.clientHeight;
    const margin = { top: 50, right: 50, bottom: 50, left: 50 };
    const chartWidth = width - margin.left - margin.right;
    const chartHeight = height - margin.top - margin.bottom;

    const svg = d3.select(chartRef.current)
      .attr('width', width)
      .attr('height', height);

    // Clear any previous renders
    svg.selectAll('*').remove();

    const chart = svg.append('g')
      .attr('transform', `translate(${margin.left}, ${margin.top})`);

    // Set scales
    const xScale = d3.scaleBand()
      .range([0, chartWidth])
      .domain(labels)
      .padding(0.4);

    const yScale = d3.scaleLinear()
      .range([chartHeight, 0])
      .domain([0, d3.max(counts)]);

    // Draw axes
    // const xAxis = d3.axisBottom(xScale);
    const yAxis = d3.axisLeft(yScale);

    // chart.append('g')
    //   .attr('transform', `translate(0, ${chartHeight})`)
    //   .call(xAxis);

    chart.append('g').call(yAxis);

    // Draw bars
    chart.selectAll(".bar")
      .data(counts.map((value, index) => ({ value, index })))  // 包装数据和索引
      .enter()
      .append('rect')
      .attr('class', 'bar')
      .attr('x', d => xScale(labels[d.index]))
      .attr('y', d => yScale(d.value))
      .attr('width', xScale.bandwidth())
      .attr('height', d => chartHeight - yScale(d.value))
      .attr('fill', 'steelblue')
      .on('mouseover', function (event, d) {
        console.log("鼠标移入", labels[d.index]);
          // 鼠标移入，显示横轴名字
          const yPos = yScale(d.value) - 10; // 将文本放在柱子的上方一点的位置
          chart.append('text')
              .attr('fill', 'red')
              .attr('id', 'tempLabel')
              .attr('x', xScale(labels[d.index]) + (xScale.bandwidth() / 2))  // 中心对齐
              .attr('y', yPos)
              .attr('text-anchor', 'middle')  // 文本居中对齐
              .text(labels[d.index]);
      })
      .on('mouseout', function (event, d) { 
          // 鼠标移出，移除之前添加的名字
          d3.select('#tempLabel').remove();
          console.log("鼠标移出")
      });
}

  return (
    <div id="chartBody">
      <div id="ccccc">123123123123</div><svg id="chart" ref={chartRef}></svg>
    </div>
  )
}

export default ChartComponent;