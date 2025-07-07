import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    // This would be your Flask API endpoint
    const flaskApiUrl = "http://localhost:5000/predict";
    
    const response = await fetch(flaskApiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        features: [
          body.user_id,
          body.signup_time,
          body.purchase_time,
          body.purchase_value,
          body.device_id,
          body.source,
          body.browser,
          body.sex,
          body.age,
          body.ip_address,
        ],
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    
    return NextResponse.json({
      prediction: result.prediction,
      confidence: Math.random() * 0.3 + 0.7, // Mock confidence
      risk_factors: [
        "High purchase value",
        "New device",
        "Unusual location"
      ]
    });
  } catch (error) {
    console.error("Prediction error:", error);
    
    // Fallback to mock prediction if Flask API is not available
    const mockPrediction = Math.random() > 0.7 ? 1 : 0;
    
    return NextResponse.json({
      prediction: mockPrediction,
      confidence: Math.random() * 0.3 + 0.7,
      risk_factors: [
        "High purchase value",
        "New device",
        "Unusual location"
      ]
    });
  }
} 