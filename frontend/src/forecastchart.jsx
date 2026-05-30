import {LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ReferenceLine, ResponsiveContainer} from "recharts"


function ForecastChart({data}){
    if(!data || !Array.isArray(data)) return null
    const chartData = data.map(d => ({
        day: `Day ${d.day}`,
        risk: Math.round(d.risk_score *100)
    }))
console.log("chartData:", chartData)
    return (
        <div style = {{background : "#0000", borderRadius:"8px", padding: "24px", marginTop:"16px"}}>
            <p style = {{color: "rgba(0, 0, 0, 0.13)", margin:"0 0 16px 0", fontSize: "25px"}}>7 DAYS WEATHER FORECAST OF LUKLA Y-Axis is Cancellation Rate, Whereas X- Axis is the number of days</p>
            <ResponsiveContainer width = "100%" height = {200}>
                <LineChart data = {chartData}>
                    <CartesianGrid strokeDasharray = "3 3" stroke = "#333"/>
                    <XAxis dataKey = "day" stroke = "#000000" fontSize = {12}/>
                    <YAxis stroke = "#00000" fontSize = {12} doman = {[0,100]} unit = "%"/>
                    <ReferenceLine y = {30} stroke = "#000000" strokeDasharray = "3 3"/>
                    <ReferenceLine y = {60} stroke = "#ffe600" strokeDasharray = "3 3"/>
                    <Line type = "monotone"  dataKey = "risk" stroke = "#00ff15" strokeWidth={2} dot = {{ fill : "#00ff15"}}/>
                </LineChart>
            </ResponsiveContainer>
        </div>
    )
}

export default ForecastChart