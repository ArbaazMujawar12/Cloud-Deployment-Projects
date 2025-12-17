const API = ''; // IMPORTANT

// Load data on page load
document.addEventListener('DOMContentLoaded', () => {
    loadExpenses();
    loadTotals();
});

// Add expense
document.getElementById('expenseForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const amount = document.getElementById('amount').value;
    const category = document.getElementById('category').value;
    const description = document.getElementById('description').value;

    const response = await fetch('/api/add-expense', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            amount: amount,
            category: category,
            description: description
        })
    });

    const data = await response.json();

    if (response.ok) {
        document.getElementById('expenseForm').reset();
        loadExpenses();
        loadTotals();
    } else {
        alert('Error adding expense');
        console.error(data);
    }
});

// Load expenses
async function loadExpenses() {
    const res = await fetch('/api/expenses');
    const expenses = await res.json();

    const table = document.getElementById('expenseTable');
    table.innerHTML = '';

    expenses.forEach(exp => {
        table.innerHTML += `
            <tr>
                <td>${exp.amount}</td>
                <td>${exp.category}</td>
                <td>${exp.description}</td>
                <td>${new Date(exp.created_at).toLocaleString()}</td>
            </tr>
        `;
    });
}

// Load totals
async function loadTotals() {
    const res = await fetch('/api/totals');
    const totals = await res.json();

    const container = document.getElementById('totals');
    container.innerHTML = '';

    totals.forEach(t => {
        container.innerHTML += `
            <div class="col-md-3 mb-3">
                <div class="card summary-card p-3 shadow-sm">
                    <h6>${t.category}</h6>
                    <h4>₹ ${t.total}</h4>
                </div>
            </div>
        `;
    });
}
