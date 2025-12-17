const express = require('express');
const router = express.Router();
const db = require('./db');

// Add Expense
router.post('/api/add-expense', (req, res) => {
    const { amount, category, description } = req.body;

    const sql = 'INSERT INTO expenses (amount, category, description) VALUES (?, ?, ?)';
    db.query(sql, [amount, category, description], (err) => {
        if (err) return res.status(500).json(err);
        res.json({ message: 'Expense added successfully' });
    });
});

// Get All Expenses
router.get('/api/expenses', (req, res) => {
    const sql = 'SELECT * FROM expenses ORDER BY created_at DESC';
    db.query(sql, (err, results) => {
        if (err) return res.status(500).json(err);
        res.json(results);
    });
});

// Smart Totals (SQL Aggregation)
router.get('/api/totals', (req, res) => {
    const sql = `
        SELECT category, SUM(amount) AS total
        FROM expenses
        GROUP BY category
    `;
    db.query(sql, (err, results) => {
        if (err) return res.status(500).json(err);
        res.json(results);
    });
});

module.exports = router;