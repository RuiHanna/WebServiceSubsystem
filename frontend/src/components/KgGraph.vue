<template>
  <svg ref="svg"></svg>
</template>
<script setup name="KgGraph">
import * as d3 from "d3";
import {onMounted, ref} from "vue";

const svg = ref(null);

onMounted(async () => {
  const res = await fetch("http://localhost:5000/graph-data");
  const data = await res.json();

  const width = window.innerWidth;
  const height = window.innerHeight;

  const svgEl = d3.select(svg.value)
      .attr("width", width)
      .attr("height", height);

  // 👉 添加 marker 箭头
  svgEl.append("defs").append("marker")
      .attr("id", "arrow")
      .attr("viewBox", "0 -5 10 10")
      .attr("refX", 24)
      .attr("refY", 0)
      .attr("markerWidth", 6)
      .attr("markerHeight", 6)
      .attr("orient", "auto")
      .append("path")
      .attr("d", "M0,-5L10,0L0,5")
      .attr("fill", "#999");

  const simulation = d3.forceSimulation(data.nodes)
      .force("link", d3.forceLink(data.links).id(d => d.id).distance(100))
      .force("charge", d3.forceManyBody().strength(-300))
      .force("center", d3.forceCenter(width / 2, height / 2));

  const link = svgEl.selectAll("line")
      .data(data.links)
      .enter().append("line")
      .attr("marker-end", "url(#arrow)")
      .style("stroke", "#999")
      .style("stroke-width", 2);

  const linkText = svgEl.selectAll(".link-text")
      .data(data.links)
      .enter().append("text")
      .attr("class", "link-text")
      .text(d => d.type)
      .style("font-size", "10px")
      .style("fill", "#555");

  // const node = svgEl.selectAll("circle")
  //     .data(data.nodes)
  //     .enter().append("circle")
  //     .attr("r", 10)
  //     .style("fill", "#69b3a2")
  //     .call(drag(simulation));
  //
  // const label = svgEl.selectAll(".node-label")
  //     .data(data.nodes)
  //     .enter().append("text")
  //     .text(d => d.properties.name || d.label) // 更直观显示名字
  //     .style("font-size", "10px")
  //     .style("fill", "#fff") // 白色文字，放在深色圆圈中更清晰
  //     .style("text-anchor", "middle") // 水平居中
  //     .style("dominant-baseline", "central") // 垂直居中
  //     .style("pointer-events", "none"); // 避免干扰鼠标拖动
  const nodeGroup = svgEl.selectAll("g")
      .data(data.nodes)
      .enter().append("g")
      .call(drag(simulation));

// 圆圈
  nodeGroup.append("circle")
      // .attr("r", 20) // 这里调整圆圈大小
      .attr("r", d => 6 + (d.properties.name?.length || d.label.length) * 5)
      .style("fill", "#69b3a2")
      .style("font-size", d => `${Math.max(8, 20 - d.properties.name.length)}px`);


// 文本
  nodeGroup.append("text")
      .text(d => d.properties.name || d.label)
      .style("font-size", "10px")
      .style("fill", "#fff")
      .style("text-anchor", "middle")
      .style("dominant-baseline", "central")
      .style("pointer-events", "none");


  simulation.on("tick", () => {
    link
        .attr("x1", d => d.source.x).attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x).attr("y2", d => d.target.y);

    nodeGroup.attr("transform", d => `translate(${d.x},${d.y})`);


    linkText
        .attr("x", d => (d.source.x + d.target.x) / 2)
        .attr("y", d => (d.source.y + d.target.y) / 2);
  });

  function drag(simulation) {
    function dragstarted(event, d) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }

    function dragged(event, d) {
      d.fx = event.x;
      d.fy = event.y;
    }

    function dragended(event, d) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }

    return d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended);
  }
});
</script>
