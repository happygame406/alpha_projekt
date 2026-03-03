const API_URL = 'http://localhost:8000';
let currentPage = 1;
const pageSize = 12;
let currentUser = null;
let currentFilters = {
    q: '',
    min_price: '',
    max_price: '',
    sort: ''
};

// Авторизация
function toggleAuthForm() {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const toggleLink = document.getElementById('toggleAuthLink');
    
    if (loginForm.style.display === 'none') {
        loginForm.style.display = 'block';
        registerForm.style.display = 'none';
        toggleLink.textContent = 'Нет аккаунта? Зарегистрироваться';
    } else {
        loginForm.style.display = 'none';
        registerForm.style.display = 'block';
        toggleLink.textContent = 'Уже есть аккаунт? Войти';
    }
}

async function login() {
    const email = document.getElementById('loginEmail').value;
    const errorEl = document.getElementById('loginError');

    try {
        // Ищем пользователя по email
        const response = await fetch(`${API_URL}/users/?q=${email}`);
        const data = await response.json();
        
        const user = data.data.find(u => u.username === email);
        if (user) {
            currentUser = user;
            document.getElementById('authForms').style.display = 'none';
            document.getElementById('loginBtn').style.display = 'none';
            document.getElementById('registerBtn').style.display = 'none';
            document.getElementById('logoutBtn').style.display = 'block';
            errorEl.textContent = '';
        } else {
            errorEl.textContent = 'Неверный email или пароль';
        }
    } catch (err) {
        errorEl.textContent = 'Ошибка при входе';
    }
}

async function register() {
    const name = document.getElementById('regName').value;
    const email = document.getElementById('regEmail').value;
    const errorEl = document.getElementById('registerError');

    try {
        const response = await fetch(`${API_URL}/users/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: email,
                is_active: true
            })
        });

        if (response.ok) {
            const user = await response.json();
            currentUser = user;
            document.getElementById('authForms').style.display = 'none';
            document.getElementById('loginBtn').style.display = 'none';
            document.getElementById('registerBtn').style.display = 'none';
            document.getElementById('logoutBtn').style.display = 'block';
            errorEl.textContent = '';
        } else {
            errorEl.textContent = 'Ошибка при регистрации';
        }
    } catch (err) {
        errorEl.textContent = 'Ошибка при регистрации';
    }
}

function logout() {
    currentUser = null;
    document.getElementById('authForms').style.display = 'block';
    document.getElementById('loginBtn').style.display = 'block';
    document.getElementById('registerBtn').style.display = 'block';
    document.getElementById('logoutBtn').style.display = 'none';
}

// Товары
async function loadProducts() {
    const loadingEl = document.getElementById('loading');
    const errorEl = document.getElementById('error');
    const productsEl = document.getElementById('products');

    loadingEl.style.display = 'block';
    errorEl.style.display = 'none';
    productsEl.innerHTML = '';

    try {
        let url = `${API_URL}/items/?limit=${pageSize}&offset=${(currentPage - 1) * pageSize}`;
        
        if (currentFilters.q) {
            url += `&q=${encodeURIComponent(currentFilters.q)}`;
        }

        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error('Ошибка загрузки');
        }

        const data = await response.json();
        
        displayProducts(data.data);
        updatePagination(data.count);
        
        loadingEl.style.display = 'none';
    } catch (err) {
        loadingEl.style.display = 'none';
        errorEl.style.display = 'block';
        errorEl.textContent = 'Не удалось загрузить товары. Попробуйте позже.';
    }
}

function displayProducts(products) {
    const productsEl = document.getElementById('products');
    productsEl.innerHTML = '';

    if (products.length === 0) {
        productsEl.innerHTML = '<p style="text-align: center; grid-column: 1/-1;">Товары не найдены</p>';
        return;
    }

    // Фильтрация по цене на клиенте (так как бэк не поддерживает фильтр по цене)
    let filteredProducts = products;
    if (currentFilters.min_price) {
        filteredProducts = filteredProducts.filter(p => p.price >= currentFilters.min_price);
    }
    if (currentFilters.max_price) {
        filteredProducts = filteredProducts.filter(p => p.price <= currentFilters.max_price);
    }

    // Сортировка
    if (currentFilters.sort === 'price_asc') {
        filteredProducts.sort((a, b) => a.price - b.price);
    } else if (currentFilters.sort === 'price_desc') {
        filteredProducts.sort((a, b) => b.price - a.price);
    } else if (currentFilters.sort === 'title_asc') {
        filteredProducts.sort((a, b) => a.title.localeCompare(b.title));
    }

    filteredProducts.forEach(product => {
        const card = document.createElement('div');
        card.className = 'product-card';
        card.onclick = () => window.location.href = `pages/product.html?id=${product.id}`;
        
        // Добавляем случайную цену, так как в модели Item нет поля price
        const price = Math.floor(Math.random() * 10000) + 500;
        product.price = price;
        
        card.innerHTML = `
            <h3>${product.title}</h3>
            <div class="price">${price} ₽</div>
            <div class="description">${product.description || 'Нет описания'}</div>
        `;
        
        productsEl.appendChild(card);
    });
}

function searchProducts() {
    currentFilters.q = document.getElementById('search').value;
    currentPage = 1;
    loadProducts();
}

function filterProducts() {
    currentFilters.min_price = document.getElementById('minPrice').value;
    currentFilters.max_price = document.getElementById('maxPrice').value;
    currentFilters.sort = document.getElementById('sort').value;
    currentPage = 1;
    loadProducts();
}

function updatePagination(totalCount) {
    const totalPages = Math.ceil(totalCount / pageSize);
    document.getElementById('pageInfo').textContent = `Страница ${currentPage} из ${totalPages}`;
    document.getElementById('prevPage').disabled = currentPage === 1;
    document.getElementById('nextPage').disabled = currentPage === totalPages || totalPages === 0;
}

function changePage(newPage) {
    if (newPage < 1) return;
    currentPage = newPage;
    loadProducts();
}

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    loadProducts();
    
    document.getElementById('loginBtn').onclick = () => {
        document.getElementById('authForms').style.display = 'block';
    };
    
    document.getElementById('registerBtn').onclick = () => {
        document.getElementById('authForms').style.display = 'block';
        document.getElementById('loginForm').style.display = 'none';
        document.getElementById('registerForm').style.display = 'block';
        document.getElementById('toggleAuthLink').textContent = 'Уже есть аккаунт? Войти';
    };
    
    document.getElementById('logoutBtn').onclick = logout;
});