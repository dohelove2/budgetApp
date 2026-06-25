const state = {
  transactions: [],
  filter: "",
};

const seedTransactions = [
  {
    date: "2026-01-05",
    type: "지출",
    category: "식비",
    description: "점심식사",
    amount: -12000,
    memo: "",
  },
  {
    date: "2026-01-07",
    type: "수입",
    category: "급여",
    description: "월급",
    amount: 3500000,
    memo: "1월급여",
  },
  {
    date: "2026-01-10",
    type: "지출",
    category: "교통",
    description: "지하철",
    amount: -1500,
    memo: "",
  },
  {
    date: "2026-01-12",
    type: "지출",
    category: "식비",
    description: "",
    amount: -5800,
    memo: "",
  },
  {
    date: "2026-01-28",
    type: "기타수입",
    category: "기타수입",
    description: "중고 판매",
    amount: 25000,
    memo: "중고마켓",
  },
];

const form = document.getElementById("transactionForm");
const tableBody = document.getElementById("transactionTable");
const monthlySummary = document.getElementById("monthlySummary");
const categoryFilter = document.getElementById("categoryFilter");
const clearFilter = document.getElementById("clearFilter");
const loadSeed = document.getElementById("loadSeed");
const balanceValue = document.getElementById("balanceValue");
const incomeValue = document.getElementById("incomeValue");
const expenseValue = document.getElementById("expenseValue");
const netValue = document.getElementById("netValue");
const transactionCount = document.getElementById("transactionCount");
const visibleCount = document.getElementById("visibleCount");

function formatMoney(value) {
  return new Intl.NumberFormat("ko-KR").format(value) + "원";
}

function addTransaction(transactions, transaction) {
  return transactions.concat([
    {
      date: transaction.date,
      type: transaction.type,
      category: transaction.category,
      description: transaction.description,
      amount: transaction.amount,
      memo: transaction.memo,
    },
  ]);
}

function getBalance(transactions) {
  return transactions.reduce((sum, transaction) => sum + transaction.amount, 0);
}

function filterByCategory(transactions, category) {
  const normalizedCategory = category.trim().toLowerCase();
  if (!normalizedCategory) {
    return transactions.slice();
  }
  return transactions.filter(
    (transaction) => transaction.category.toLowerCase() === normalizedCategory,
  );
}

function monthlySummary(transactions) {
  const summary = {};
  for (const transaction of transactions) {
    const month = transaction.date.slice(0, 7);
    if (!summary[month]) {
      summary[month] = { income: 0, expense: 0, net: 0 };
    }
    summary[month].net += transaction.amount;
    if (transaction.amount >= 0) {
      summary[month].income += transaction.amount;
    } else {
      summary[month].expense += transaction.amount;
    }
  }
  return summary;
}

function render() {
  const filtered = filterByCategory(state.transactions, state.filter);
  const balance = getBalance(state.transactions);
  const summary = monthlySummary(state.transactions);
  const income = state.transactions
    .filter((transaction) => transaction.amount >= 0)
    .reduce((sum, transaction) => sum + transaction.amount, 0);
  const expense = state.transactions
    .filter((transaction) => transaction.amount < 0)
    .reduce((sum, transaction) => sum + transaction.amount, 0);

  balanceValue.textContent = formatMoney(balance);
  transactionCount.textContent = `${state.transactions.length}건의 거래`;
  visibleCount.textContent = `${filtered.length}건 표시 중`;
  incomeValue.textContent = formatMoney(income);
  expenseValue.textContent = formatMoney(expense);
  netValue.textContent = formatMoney(balance);

  tableBody.innerHTML = filtered
    .map(
      (transaction) => `
        <tr>
          <td>${transaction.date}</td>
          <td>${transaction.type}</td>
          <td>${transaction.category}</td>
          <td>${transaction.description || "-"}</td>
          <td class="${transaction.amount >= 0 ? "money--income" : "money--expense"}">
            ${formatMoney(transaction.amount)}
          </td>
          <td>${transaction.memo || "-"}</td>
        </tr>
      `,
    )
    .join("");

  const sortedMonths = Object.keys(summary).sort();
  monthlySummary.innerHTML = sortedMonths
    .map(
      (month) => `
        <article class="months__item">
          <div class="months__title">${month}</div>
          <div class="months__stats">
            <div><span>수입</span><strong>${formatMoney(summary[month].income)}</strong></div>
            <div><span>지출</span><strong>${formatMoney(summary[month].expense)}</strong></div>
            <div><span>순이익</span><strong>${formatMoney(summary[month].net)}</strong></div>
          </div>
        </article>
      `,
    )
    .join("");
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  const transaction = {
    date: String(formData.get("date")),
    type: String(formData.get("type")),
    category: String(formData.get("category")).trim(),
    description: String(formData.get("description")).trim(),
    amount: Number(formData.get("amount")),
    memo: String(formData.get("memo")).trim(),
  };

  state.transactions = addTransaction(state.transactions, transaction);
  form.reset();
  render();
});

categoryFilter.addEventListener("input", (event) => {
  state.filter = event.target.value;
  render();
});

clearFilter.addEventListener("click", () => {
  state.filter = "";
  categoryFilter.value = "";
  render();
});

loadSeed.addEventListener("click", () => {
  state.transactions = seedTransactions.slice();
  render();
});

state.transactions = seedTransactions.slice();
render();
