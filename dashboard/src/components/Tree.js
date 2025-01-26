import React, { useEffect, useRef } from "react";
import * as d3 from "d3";

const DecisionTree = ({ fulldata, highlightNodes = [] }) => {
  const svgRef = useRef();

  useEffect(() => {
    const width = 2500;
    const height = 700;
    const margin = { top: 50, right: 50, bottom: 50, left: 50 };

    const data = fulldata.d3tree;

    const svg = d3
      .select(svgRef.current)
      .attr("width", width)
      .attr("height", height);

    const root = d3.hierarchy(data);

    const treeLayout = d3
      .tree()
      .size([
        width - margin.left - margin.right,
        height - margin.top - margin.bottom,
      ]);
    treeLayout(root);

    // Criação do grupo para a árvore
    const g = svg
      .append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    // Limpeza ao aplicar zoom
    const zoom = d3
      .zoom()
      .scaleExtent([0.5, 3]) // Limita o nível de zoom
      .on("zoom", function (event) {
        g.attr("transform", event.transform); // Aplica a transformação (zoom e pan)
      });

    svg.call(zoom); // Aplica o zoom ao SVG

    const initialTransform = d3.zoomIdentity.translate(0, 50).scale(0.4);
    svg.call(zoom.transform, initialTransform);

    // Desenha as arestas (linhas entre os nós)
    const links = g
      .selectAll(".link")
      .data(root.links())
      .enter()
      .append("path")
      .attr("class", "link")
      .attr(
        "d",
        d3
          .linkVertical()
          .x((d) => d.x)
          .y((d) => d.y)
      )
      .attr("fill", "none")
      .attr("stroke", "#ccc")
      .attr("stroke-width", 2);

    // Desenha os nós
    const nodes = g
      .selectAll(".node")
      .data(root.descendants())
      .enter()
      .append("g")
      .attr("class", "node")
      .attr("transform", (d) => `translate(${d.x},${d.y})`);

    nodes.append("title").text((d) => d.data.name);

    // Retângulos arredondados nos nós
    nodes
      .append("rect")
      .attr("width", 100)
      .attr("height", 50)
      .attr("x", -50)
      .attr("y", -25)
      .attr("rx", 10)
      .attr("ry", 10)
      .attr("fill", (d) =>
        highlightNodes.includes(d.data.name) ? "#FFFF00" : "#fff"
      )
      .attr("stroke", "#007bff")
      .attr("stroke-width", 2);

    // Texto dentro dos nós
    nodes
      .append("text")
      .attr("dy", "0.35em")
      .attr("text-anchor", "middle")
      .attr("font-size", "12px")
      .text((d) => d.data.condition);

    // Adiciona rótulos nas arestas (True/False)
    g.selectAll(".link-label")
      .data(root.links())
      .enter()
      .append("text")
      .attr("font-size", "12px")
      .attr("class", "link-label")
      .attr("x", (d) => (d.source.x + d.target.x) / 2)
      .attr("y", (d) => (d.source.y + d.target.y) / 2)
      .attr("text-anchor", "middle")
      .attr("dy", -5)
      .text((d, i) => (i % 2 === 0 ? "True" : "False"));

    // Remover o conteúdo da árvore e recriar ao renderizar novamente
    return () => {
      svg.selectAll("*").remove(); // Limpar a árvore antes de renderizar novamente
    };
  }, [fulldata, highlightNodes]);

  return (
    <div
      style={{
        width: "100%",
        height: "40%",
        border: "1px solid #ccc",
        overflow: "hidden",
      }}
    >
      <svg ref={svgRef}></svg>
    </div>
  );
};

export default DecisionTree;
