import { useState } from "react";
import api from "../api";
import JumpAnalyzer from "../components/JumpAnalyzer";
import "../styles/Home.css";

function Home() {
  return (
    <div className="home">
      <h1>Jump Analyzer</h1>
      <JumpAnalyzer />
    </div>
  );
}

export default Home;