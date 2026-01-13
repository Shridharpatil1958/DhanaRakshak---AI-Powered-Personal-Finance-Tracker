// DhanaRakshak Dashboard JavaScript - Modern Theme Edition

let charts = {};

// Modern color palette
const colors = {
    primary: {
        main: '#8b5cf6',
        light: '#a78bfa',
        gradient: ['#8b5cf6', '#ec4899']
    },
    success: {
        main: '#10b981',
        light: '#34d399',
        gradient: ['#10b981', '#34d399']
    },
    danger: {
        main: '#f43f5e',
        light: '#fb7185',
        gradient: ['#f43f5e', '#fb7185']
    },
    warning: {
        main: '#f59e0b',
        light: '#fbbf24',
        gradient: ['#f59e0b', '#fbbf24']
    },
    info: {
        main: '#06b6d4',
        light: '#22d3ee',
        gradient: ['#06b6d4', '#22d3ee']
    },
    chart: [
        '#8b5cf6', '#ec4899', '#06b6d4', '#f59e0b', 
        '#10b981', '#f43f5e', '#a78bfa', '#22d3ee',
        '#fbbf24', '#34d399'
    ]
};

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    loadDashboardData();
    initializeAnimations();

    // Auto-run predictions
    predictExpenses();
    predictSavings();
    estimateBills();
    detectAnomalies();
});

// Load dashboard data
async function loadDashboardData() {
    try {
        const response = await fetch('/api/dashboard/data');
        const data = await response.json();

        // Check if data exists, else provide empty placeholders
        const monthlyExpenses = data.monthly_expenses || { labels: [], values: [] };
        const categorySpending = data.category_spending || { labels: [], values: [] };
        const incomeVsExpense = data.income_vs_expense || { labels: [], income: [], expense: [] };
        const spendingDistribution = data.spending_distribution || { labels: [], values: [] };

        // Create charts with modern styling
        createMonthlyExpenseChart(monthlyExpenses);
        createCategoryChart(categorySpending);
        createIncomeExpenseChart(incomeVsExpense);
        createDistributionChart(spendingDistribution);

    } catch (error) {
        console.error('Error loading dashboard data:', error);
    }
}

// Chart.js default configuration
Chart.defaults.color = '#9ca3af';
Chart.defaults.borderColor = 'rgba(139, 92, 246, 0.2)';
Chart.defaults.font.family = "'Inter', 'Segoe UI', system-ui, sans-serif";

// Common chart options
const commonOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            display: true,
            position: 'top',
            labels: {
                padding: 15,
                usePointStyle: true,
                font: {
                    size: 12,
                    weight: '600'
                }
            }
        },
        tooltip: {
            backgroundColor: 'rgba(15, 23, 42, 0.95)',
            titleColor: '#f3f4f6',
            bodyColor: '#d1d5db',
            borderColor: 'rgba(139, 92, 246, 0.5)',
            borderWidth: 1,
            padding: 12,
            cornerRadius: 8,
            displayColors: true,
            titleFont: {
                size: 14,
                weight: 'bold'
            },
            bodyFont: {
                size: 13
            }
        }
    }
};

// Monthly Expense Chart (Gradient Line)
function createMonthlyExpenseChart(data) {
    const ctx = document.getElementById('monthlyExpenseChart');
    if (!ctx) return;

    if (charts.monthlyExpense) charts.monthlyExpense.destroy();

    // Create gradient
    const gradient = ctx.getContext('2d').createLinearGradient(0, 0, 0, 300);
    gradient.addColorStop(0, 'rgba(139, 92, 246, 0.3)');
    gradient.addColorStop(0.5, 'rgba(139, 92, 246, 0.1)');
    gradient.addColorStop(1, 'rgba(139, 92, 246, 0)');

    charts.monthlyExpense = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Monthly Expenses',
                data: data.values,
                borderColor: '#8b5cf6',
                backgroundColor: gradient,
                borderWidth: 3,
                tension: 0.4,
                fill: true,
                pointRadius: 5,
                pointHoverRadius: 8,
                pointBackgroundColor: '#8b5cf6',
                pointBorderColor: '#ffffff',
                pointBorderWidth: 2,
                pointHoverBackgroundColor: '#ec4899',
                pointHoverBorderColor: '#ffffff',
                pointHoverBorderWidth: 3
            }]
        },
        options: {
            ...commonOptions,
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(139, 92, 246, 0.1)',
                        drawBorder: false
                    },
                    ticks: {
                        callback: value => '₹' + value.toLocaleString('en-IN'),
                        padding: 10
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        padding: 10
                    }
                }
            },
            plugins: {
                ...commonOptions.plugins,
                tooltip: {
                    ...commonOptions.plugins.tooltip,
                    callbacks: {
                        label: function(ctx) {
                            return 'Expenses: ₹' + (ctx.parsed.y || 0).toLocaleString('en-IN');
                        }
                    }
                }
            }
        }
    });
}

// Category Chart (Doughnut with gradient colors)
function createCategoryChart(data) {
    const ctx = document.getElementById('categoryChart');
    if (!ctx) return;

    if (charts.category) charts.category.destroy();

    charts.category = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: data.labels,
            datasets: [{
                data: data.values,
                backgroundColor: colors.chart,
                borderColor: 'rgba(15, 23, 42, 0.8)',
                borderWidth: 3,
                hoverOffset: 15,
                hoverBorderColor: '#ffffff',
                hoverBorderWidth: 3
            }]
        },
        options: {
            ...commonOptions,
            cutout: '65%',
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        padding: 15,
                        usePointStyle: true,
                        pointStyle: 'circle',
                        font: {
                            size: 12,
                            weight: '600'
                        }
                    }
                },
                tooltip: {
                    ...commonOptions.plugins.tooltip,
                    callbacks: {
                        label: function(ctx) {
                            const label = ctx.label || '';
                            const value = ctx.parsed || 0;
                            const total = ctx.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = total ? ((value / total) * 100).toFixed(1) : 0;
                            return `${label}: ₹${value.toLocaleString('en-IN')} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// Income vs Expense Chart (Gradient Bars)
function createIncomeExpenseChart(data) {
    const ctx = document.getElementById('incomeExpenseChart');
    if (!ctx) return;

    if (charts.incomeExpense) charts.incomeExpense.destroy();

    charts.incomeExpense = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [
                {
                    label: 'Income',
                    data: data.income || [],
                    backgroundColor: '#10b981',
                    borderColor: '#34d399',
                    borderWidth: 2,
                    borderRadius: 8,
                    borderSkipped: false
                },
                {
                    label: 'Expense',
                    data: data.expense || [],
                    backgroundColor: '#f43f5e',
                    borderColor: '#fb7185',
                    borderWidth: 2,
                    borderRadius: 8,
                    borderSkipped: false
                }
            ]
        },
        options: {
            ...commonOptions,
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(139, 92, 246, 0.1)',
                        drawBorder: false
                    },
                    ticks: {
                        callback: value => '₹' + value.toLocaleString('en-IN'),
                        padding: 10
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        padding: 10
                    }
                }
            },
            plugins: {
                ...commonOptions.plugins,
                tooltip: {
                    ...commonOptions.plugins.tooltip,
                    callbacks: {
                        label: ctx => `${ctx.dataset.label}: ₹${(ctx.parsed.y || 0).toLocaleString('en-IN')}`
                    }
                }
            }
        }
    });
}

// Spending Distribution Chart (Gradient Bars)
function createDistributionChart(data) {
    const ctx = document.getElementById('distributionChart');
    if (!ctx) return;

    if (charts.distribution) charts.distribution.destroy();

    // Create gradient for bars
    const gradient = ctx.getContext('2d').createLinearGradient(0, 0, 0, 300);
    gradient.addColorStop(0, '#06b6d4');
    gradient.addColorStop(1, '#8b5cf6');

    charts.distribution = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Transactions',
                data: data.values || [],
                backgroundColor: gradient,
                borderColor: '#22d3ee',
                borderWidth: 2,
                borderRadius: 8,
                borderSkipped: false
            }]
        },
        options: {
            ...commonOptions,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    ...commonOptions.plugins.tooltip,
                    callbacks: {
                        label: ctx => `Transactions: ${ctx.parsed.y}`
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1,
                        padding: 10
                    },
                    grid: {
                        color: 'rgba(139, 92, 246, 0.1)',
                        drawBorder: false
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        padding: 10
                    }
                }
            }
        }
    });
}

// Initialize animations
function initializeAnimations() {
    // Counter animation for stat values
    const statValues = document.querySelectorAll('.stat-value');
    statValues.forEach(element => {
        animateValue(element);
    });
}

// Animate number counting
function animateValue(element) {
    const text = element.textContent;
    const match = text.match(/₹?([\d,]+\.?\d*)/);
    
    if (!match) return;
    
    const target = parseFloat(match[1].replace(/,/g, ''));
    const duration = 1500;
    const increment = target / (duration / 16);
    let current = 0;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        element.textContent = text.replace(match[0], '₹' + current.toLocaleString('en-IN', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        }));
    }, 16);
}

// Helper: Currency formatting
function formatCurrency(amount) {
    return '₹' + (amount || 0).toLocaleString('en-IN', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}

// --- AI Prediction Placeholders ---
async function predictExpenses() {
    // Placeholder for expense prediction
    console.log('Predicting future expenses...');
}

async function predictSavings() {
    // Placeholder for savings prediction
    console.log('Predicting savings goals...');
}

async function estimateBills() {
    // Placeholder for bill estimation
    console.log('Estimating upcoming bills...');
}

async function detectAnomalies() {
    // Placeholder for anomaly detection
    console.log('Detecting spending anomalies...');
}

// Smooth scroll to section
function scrollToSection(sectionId) {
    const element = document.getElementById(sectionId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

// Export for external use
window.dashboardCharts = charts;
window.refreshCharts = loadDashboardData;