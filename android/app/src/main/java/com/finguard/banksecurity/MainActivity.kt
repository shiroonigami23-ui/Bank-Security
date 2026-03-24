package com.finguard.banksecurity

import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.Spinner
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    private lateinit var amountInput: EditText
    private lateinit var probabilityInput: EditText
    private lateinit var countryInput: EditText
    private lateinit var velocitySpinner: Spinner
    private lateinit var analyzeButton: Button
    private lateinit var simulateButton: Button
    private lateinit var resultText: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        amountInput = findViewById(R.id.amount_input)
        probabilityInput = findViewById(R.id.probability_input)
        countryInput = findViewById(R.id.country_input)
        velocitySpinner = findViewById(R.id.velocity_spinner)
        analyzeButton = findViewById(R.id.analyze_button)
        simulateButton = findViewById(R.id.simulate_button)
        resultText = findViewById(R.id.result_text)

        analyzeButton.setOnClickListener {
            val amount = amountInput.text.toString().toDoubleOrNull()
            val probabilityPct = probabilityInput.text.toString().toDoubleOrNull()
            val country = countryInput.text.toString().trim().uppercase()
            val velocity = velocitySpinner.selectedItem.toString()

            if (amount == null || probabilityPct == null || country.isEmpty()) {
                resultText.text = getString(R.string.validation_error)
                return@setOnClickListener
            }

            val risk = calculateRiskScore(amount, probabilityPct / 100.0, country, velocity)
            resultText.text = formatResult(amount, country, velocity, risk)
        }

        simulateButton.setOnClickListener {
            amountInput.setText("7850")
            probabilityInput.setText("63.4")
            countryInput.setText("RU")
            velocitySpinner.setSelection(2)
            val risk = calculateRiskScore(7850.0, 0.634, "RU", "High")
            resultText.text = formatResult(7850.0, "RU", "High", risk)
        }
    }

    private fun calculateRiskScore(amount: Double, probability: Double, country: String, velocity: String): Double {
        var risk = probability

        risk *= when {
            amount > 10000 -> 1.30
            amount > 5000 -> 1.15
            else -> 1.0
        }

        if (country in setOf("RU", "CN", "NG", "VE")) {
            risk *= 1.25
        }

        risk *= when (velocity) {
            "High" -> 1.20
            "Extreme" -> 1.40
            else -> 1.0
        }

        return risk.coerceAtMost(1.0)
    }

    private fun formatResult(amount: Double, country: String, velocity: String, risk: Double): String {
        val riskPct = String.format("%.2f", risk * 100)
        val decision = if (risk >= 0.65) "BLOCK / REVIEW" else "APPROVE"
        return """
            Offline Transaction Analysis
            Amount: EUR ${String.format("%.2f", amount)}
            Country: $country
            Velocity: $velocity
            Risk Score: $riskPct%
            Decision: $decision
        """.trimIndent()
    }
}
