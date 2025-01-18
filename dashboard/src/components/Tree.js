import React, { useEffect, useRef } from "react";
import * as d3 from "d3";

const DecisionTree = ({ decisionPath }) => {
  const svgRef = useRef(null); // Ref para o SVG

  useEffect(() => {
    const width = 800;
    const height = 600;

    // Dados da árvore de decisão (exemplo simples)
    const treeData = {
      name: "PL2 <= 16002",
      children: [
        {
          name: "LDA1 <= -0.636",
          children: [{ name: "G2" }],
        },
        {
          name: "G1",
        },
      ],
    };

    // Criação do SVG para desenhar a árvore
    const svg = d3
      .select(svgRef.current)
      .attr("width", width)
      .attr("height", height);

    // Estrutura hierárquica da árvore
    const root = d3.hierarchy(treeData);
    const treeLayout = d3.tree().size([width - 100, height - 100]);
    treeLayout(root);

    // Criação das arestas (linhas)
    svg
      .selectAll(".link")
      .data(root.links())
      .join("line")
      .attr("class", "link")
      .attr("x1", (d) => d.source.x + 50)
      .attr("y1", (d) => d.source.y + 50)
      .attr("x2", (d) => d.target.x + 50)
      .attr("y2", (d) => d.target.y + 50)
      .attr("stroke", "#ccc")
      .attr("stroke-width", 2);

    // Adiciona texto nas arestas.
    svg
      .selectAll(".link-text")
      .data(root.links())
      .join("text")
      .attr("class", "link-text")
      .attr("x", (d) => (d.source.y + d.target.y) / 2 + 200)
      .attr("y", (d) => (d.source.x + d.target.x) / 2 - 100)
      .attr("dy", "-0.5em")
      .attr("text-anchor", "middle")
      .text((d, i) => `Aresta ${i + 1}`) // Substitua com seus nomes específicos.
      .attr("fill", "#666");

    // Criação dos nós (círculos)
    svg
      .selectAll(".node")
      .data(root.descendants())
      .join("square")
      .attr("class", "node")
      .attr("cx", (d) => d.x + 50)
      .attr("cy", (d) => d.y + 50)
      .attr("r", 10)
      .attr("fill", (d) =>
        decisionPath.includes(d.data.name) ? "green" : "blue"
      );

    // Adicionando texto aos nós
    svg
      .selectAll(".node-text")
      .data(root.descendants())
      .join("text")
      .attr("class", "node-text")
      .attr("x", (d) => d.x + 50)
      .attr("y", (d) => d.y + 35)
      .attr("text-anchor", "middle")
      .attr("font-size", "12px")
      .attr("fill", "#000")
      .text((d) => d.data.name);

    // Adicionando as decisões de forma mais clara
    svg
      .selectAll(".decision-text")
      .data(root.descendants())
      .join("text")
      .attr("class", "decision-text")
      .attr("x", (d) => d.x + 50)
      .attr("y", (d) => d.y + 65)
      .attr("text-anchor", "middle")
      .attr("font-size", "10px")
      .attr("fill", "#888")
      .text((d) => {
        // Exibindo a decisão associada ao nó
        if (d.data.name === "Decision 1") return "Decision 1";
        if (d.data.name === "Decision 2") return "Decision 2";
        return "";
      });
  }, [decisionPath]);

  return (
    <div className="row">
      <div className="col">
        <svg ref={svgRef}></svg>
      </div>
    </div>
  );
};

export default DecisionTree;
