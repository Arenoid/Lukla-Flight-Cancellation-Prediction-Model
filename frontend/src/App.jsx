import { use, useEffect, useState } from "react";
import axios from "axios"
import ForecastChart from "./forecastchart";

function getRiskColor(label){
  if(label === "Low") return "#00ff15"
  if(label === "Medium") return "#ffe600"
  return "#ff0000"
}

function App(){
  const[weather,setWeather] = useState(null)
  const[risk, setRisk] = useState(null)
  const[forecast, setForecast] = useState(null)


useEffect(() => {
axios.get("https://lukla-flight-cancellation-prediction.onrender.com/current").then(res => setWeather(res.data))
axios.get("https://lukla-flight-cancellation-prediction.onrender.com/predict").then(res => setRisk(res.data))
axios.get("https://lukla-flight-cancellation-prediction.onrender.com/forecast").then(res => setForecast(res.data))
}, [])

console.log("forecast:", forecast)

  return(
  <div style={{fontFamily: "monospace", padding:"32px", background:"cyan", minHeight: "100vh", color:"white", boxSizing: "border-box", width:"100%"}}>
  <h1 style = {{fontSize: "24px", marginBottom:"8px"}}>Lukla Weather Dashboard</h1>
  <p style={{ color: "#888", marginBottom: "32px"}}>Model to predict flight cancellation risk</p>
  
  {risk &&(
    <div style = {{background: "#000000", borderRadius: "8px", padding:"32px", textAlign:"Center"}}>
   <p style={{ color: "#72727288", marginBottom:"4px"}}>Flight Cancellation Risk</p>
   <h2 style = {{fontSize: "48px", margin:0, color:getRiskColor(risk.label),margin:0}}>{risk.label.toUpperCase()}</h2>
   <p style = {{ color: "#8888", marginTop:"8rem"}}>Risk Score: {(risk.risk_score *100).toFixed(1)}%</p>
   </div>
  )}
  {weather && (
    <div style={{display:"grid", gridTemplateColumns: "repeat(2,1fr)", gap:"16px"}}>
      {[
        {label: "Temperature", value: `${weather.temperature_2m}°C`},
        {label: "Wind Speed", value: `${weather.wind_speed_10m} m/s` },
        {label: "Cloud Cover", value: `${weather.cloud_cover}%` },
        {label: "Pressure", value: `${weather.surface_pressure}hPa` },
          ].map(item => (
            <div key={item.label} style = {{background:'#000000', borderRadius: "10px", padding:"16px"}}>
              <p style={{color:"#66666688", margin:0, fontSize: "12px"}}>{item.label}</p>
              <p style={{margin:0, fontSize: "24px"}}>{item.value}</p>
            </div>
          ))}
          </div>      
  )}
  {!weather && !risk && <p>Loading...</p>}
  {forecast && <ForecastChart data = {forecast}/>}
</div>
)}
export default App