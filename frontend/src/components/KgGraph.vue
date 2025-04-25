<template>
    <el-container style="height: 100vh">
        <!-- 顶部导航栏 -->
        <el-header height="60px"
                   style="background-color: #409EFF; color: white; display: flex; align-items: center; justify-content: space-between; padding: 0 20px;">
            <div style="font-size: 20px; font-weight: bold">知识图谱可视化</div>
            <div>
                <el-button type="primary" text @click="goTo('/page1')">页面一</el-button>
                <el-button type="primary" text @click="goTo('/page2')">页面二</el-button>
                <el-button type="primary" text @click="goTo('/page3')">页面三</el-button>
            </div>
        </el-header>

        <el-container>
            <!-- 侧边栏 -->
            <el-aside width="250px" style="background-color: #f5f5f5; padding: 20px;">
                <h3>工具栏</h3>
                <el-dropdown @command="saveAs">
                    <el-button type="primary">保存图片</el-button>
                    <template #dropdown>
                        <el-dropdown-menu>
                            <el-dropdown-item command="svg">保存为 SVG</el-dropdown-item>
                            <el-dropdown-item command="png">保存为 PNG</el-dropdown-item>
                        </el-dropdown-menu>
                    </template>
                </el-dropdown>

                <el-button @click="zoom(1.2)" style="margin-bottom: 10px;">放大</el-button>
                <el-button @click="zoom(0.8)" style="margin-bottom: 10px;">缩小</el-button>

                <h3 style="margin-top: 20px;">节点详情</h3>
                <div v-if="selectedNode">
                    <p><strong>{{ selectedNode.name }}</strong></p>
                    <ul>
                        <li v-for="(val, key) in selectedNode.properties" :key="key">{{ key }}: {{ val }}</li>
                    </ul>
                </div>
                <div v-else>
                    <p>点击节点查看详情</p>
                </div>
            </el-aside>

            <!-- 图谱区域 -->
            <el-main>
                <svg ref="svg"></svg>
            </el-main>
        </el-container>
    </el-container>
</template>

<script setup>
import * as d3 from "d3";
import {onMounted, ref} from "vue";
import {useRouter} from 'vue-router';

const router = useRouter();
const goTo = (path) => router.push(path);

const svg = ref(null);
const selectedNode = ref(null);
let zoomGroup, simulation, zoomHandler;

//挂载
onMounted(async () => {
    const res = await fetch("http://localhost:5000/graph-data");
    const data = await res.json();

    const width = window.innerWidth - 250; // 减去 aside 宽度
    const height = window.innerHeight - 60; // 减去 header 高度

    const svgEl = d3.select(svg.value)
        .attr("width", width)
        .attr("height", height);

    svgEl.selectAll("*").remove(); // 清空旧图

    zoomHandler = d3.zoom().on("zoom", (event) => {
        zoomGroup.attr("transform", event.transform);
    });
    svgEl.call(zoomHandler);

    // 添加箭头
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

    zoomGroup = svgEl.append("g");

    simulation = d3.forceSimulation(data.nodes)
        .force("link", d3.forceLink(data.links).id(d => d.id).distance(100))
        .force("charge", d3.forceManyBody().strength(-300))
        .force("center", d3.forceCenter(width / 2, height / 2));

    const link = zoomGroup.selectAll("line")
        .data(data.links)
        .enter().append("line")
        .attr("marker-end", "url(#arrow)")
        .style("stroke", "#999");

    const linkText = zoomGroup.selectAll(".link-text")
        .data(data.links)
        .enter().append("text")
        .text(d => d.type)
        .style("font-size", "10px").style("fill", "#555");

    const nodeGroup = zoomGroup.selectAll("g")
        .data(data.nodes)
        .enter().append("g")
        .call(drag(simulation))
        .on("click", (_, d) => selectedNode.value = d);

    nodeGroup.append("circle")
        .attr("r", d => 6 + (d.properties.name?.length || d.label.length) * 5)
        .style("fill", d => d.label === "Person" ? "#69b3a2" : "#ff7f0e") // Person青绿，Artifact橙色

    nodeGroup.append("text")
        .text(d => d.name || d.label)
        .style("fill", "white")
        .style("font-size", "12px")
        .style("text-anchor", "middle")
        .style("dominant-baseline", "central")
        .style("pointer-events", "none");

    simulation.on("tick", () => {
        link.attr("x1", d => d.source.x)
            .attr("y1", d => d.source.y)
            .attr("x2", d => d.target.x)
            .attr("y2", d => d.target.y);

        linkText
            .attr("x", d => (d.source.x + d.target.x) / 2)
            .attr("y", d => (d.source.y + d.target.y) / 2);

        nodeGroup.attr("transform", d => `translate(${d.x},${d.y})`);
    });
});

//拖拽管理
function drag(simulation) {
    return d3.drag()
        .on("start", (event, d) => {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        })
        .on("drag", (event, d) => {
            d.fx = event.x;
            d.fy = event.y;
        })
        .on("end", (event, d) => {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        });
}

//缩放管理
function zoom(factor) {
    const svgEl = d3.select(svg.value);
    svgEl.transition().duration(300).call(zoomHandler.scaleBy, factor);
}


//保存图片
function saveAs(type) {
    const svgElement = svg.value;
    const svgData = new XMLSerializer().serializeToString(svgElement);

    if (type === 'svg') {
        const blob = new Blob([svgData], {type: "image/svg+xml;charset=utf-8"});
        const a = document.createElement("a");
        a.href = URL.createObjectURL(blob);
        a.download = "graph.svg";
        a.click();
        return;
    }

    if (type === 'png') {
        const canvas = document.createElement("canvas");
        const ctx = canvas.getContext("2d");
        const img = new Image();
        const svgSize = svgElement.getBoundingClientRect();
        canvas.width = svgSize.width;
        canvas.height = svgSize.height;

        img.onload = () => {
            ctx.drawImage(img, 0, 0);
            const a = document.createElement("a");
            a.download = "graph.png";
            a.href = canvas.toDataURL("image/png");
            a.click();
        };
        img.src = "data:image/svg+xml;base64," + btoa(unescape(encodeURIComponent(svgData)));
    }
}

</script>

<style scoped>
el-header .el-button + .el-button {
    margin-left: 10px;
}
</style>
