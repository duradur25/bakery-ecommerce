/**
 * api.js — La Pâtisserie · FastAPI Client
 * ─────────────────────────────────────────────────────────────────────────────
 * Disesuaikan dengan struktur backend FastAPI milik La Pâtisserie.
 *
 * Cara pakai di home.html (sudah terpasang via <script type="module">):
 *   import { api } from './api.js';
 *
 * Ubah BASE_URL di bawah sesuai alamat server FastAPI.
 * Development : 'http://localhost:8000'
 * Production  : 'https://api.lapatisserie.id'   ← contoh
 */

// ═══════════════════════════════════════════════════════════════════════
//  KONFIGURASI — UBAH SESUAI KEBUTUHAN
// ═══════════════════════════════════════════════════════════════════════
const BASE_URL  = 'http://localhost:8000'; // ← URL FastAPI
const TOKEN_KEY = 'lp_access_token';       // kunci localStorage untuk JWT


// ═══════════════════════════════════════════════════════════════════════
//  INTERNAL HELPERS
// ═══════════════════════════════════════════════════════════════════════

function getToken()   { return localStorage.getItem(TOKEN_KEY) ?? null; }
function setToken(t)  { localStorage.setItem(TOKEN_KEY, t); }
function clearToken() { localStorage.removeItem(TOKEN_KEY); }

async function request(endpoint, opts = {}) {
  const token = getToken();

  const response = await fetch(`${BASE_URL}${endpoint}`, {
    ...opts,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(opts.headers ?? {}),
    },
  });

  if (response.status === 401) {
    clearToken();
    window.dispatchEvent(new CustomEvent('lp:unauthorized'));
    throw new Error('Sesi telah berakhir. Silakan login kembali.');
  }

  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail ?? `HTTP ${response.status} — ${response.statusText}`);
  }

  if (response.status === 204) return null;

  return response.json();
}


// ═══════════════════════════════════════════════════════════════════════
//  AUTH  —  /register  |  /login
// ═══════════════════════════════════════════════════════════════════════
const auth = {
  async register({ nama_lengkap, email, password, conf_pass }) {
    return request('/register', {
      method: 'POST',
      body: JSON.stringify({ nama_lengkap, email, password, conf_pass }),
    });
  },

  async login({ email, password }) {
    const result = await request('/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    if (result?.access_token) setToken(result.access_token);
    return result;
  },

  async logout() {
    clearToken();
    window.dispatchEvent(new CustomEvent('lp:logout'));
  },

  isLoggedIn() { return !!getToken(); },
};


// ═══════════════════════════════════════════════════════════════════════
//  PRODUK / KERANJANG / PESANAN / TESTIMONI / SARAN
// ═══════════════════════════════════════════════════════════════════════
const produk = {
  async getAll(kategori) {
    const q = kategori ? `?kategori=${encodeURIComponent(kategori)}` : '';
    return request(`/produk${q}`);
  },
  async getById(id) { return request(`/produk/${id}`); },
};

const keranjang = {
  async get()               { return request('/keranjang'); },
  async tambah(data)        { return request('/keranjang/item',           { method: 'POST',   body: JSON.stringify(data) }); },
  async update(itemId, data){ return request(`/keranjang/item/${itemId}`, { method: 'PUT',    body: JSON.stringify(data) }); },
  async hapusItem(itemId)   { return request(`/keranjang/item/${itemId}`, { method: 'DELETE' }); },
  async kosongkan()         { return request('/keranjang',                { method: 'DELETE' }); },
  async checkout(data)      { return request('/pesanan',                  { method: 'POST',   body: JSON.stringify(data) }); },
};

const pesanan = {
  async getAll()    { return request('/pesanan'); },
  async getById(id) { return request(`/pesanan/${id}`); },
};

const testimoni = {
  async getAll()    { return request('/testimoni'); },
  async kirim(data) { return request('/testimoni', { method: 'POST', body: JSON.stringify(data) }); },
};

const saran = {
  async kirim(data) { return request('/saran', { method: 'POST', body: JSON.stringify(data) }); },
};


// ═══════════════════════════════════════════════════════════════════════
//  EXPORT
// ═══════════════════════════════════════════════════════════════════════
export const api = {
  auth, produk, keranjang, pesanan, testimoni, saran,
  _getToken: getToken, _setToken: setToken, _clearToken: clearToken,
};