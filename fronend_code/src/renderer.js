window.onload = function() {
    fetchDataAndDrawChart();
    setInterval(fetchDataAndDrawChart, 1000); // 每1秒调用一次

    // 监听窗口大小变化，并重新获取数据和绘制图表
    window.addEventListener('resize', fetchDataAndDrawChart);
}



function fetchDataAndDrawChart() {
    fetch('http://127.0.0.1:12310/get_chart_data/')
    .then(response => response.json())
    .then(data => {
        d3.select("#chart").html(""); // 清空SVG元素
        drawChart(data.labels, data.counts);
    });
}

function drawChart(labels, counts) {
    const width = document.documentElement.clientWidth;
    const height = document.documentElement.clientHeight;

    const svg = d3.select("#chart")
        .attr('width', width)
        .attr('height', height);

    const xScale = d3.scaleBand()
        .domain(labels)
        .range([0, width])
        .padding(0.2);
    
    const yScale = d3.scaleLinear()
        .domain([0, d3.max(counts)])
        .range([height, 0]);

    svg.selectAll('rect')
        .data(counts)
        .enter()
        .append('rect')
        .attr('x', (d, i) => xScale(labels[i]))
        .attr('y', d => yScale(d))
        .attr('width', xScale.bandwidth())
        .attr('height', d => height - yScale(d))
        .attr('fill', 'steelblue');

    // 更多图表的定制，例如添加轴、标签等。
}
