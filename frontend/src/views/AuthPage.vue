<template>
  <div class="auth-container">
    <div class="auth-box">
      <div class="auth-header">
        <div class="auth-logo">
          <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
          </svg>
          <div class="logo-text">
            <h1>AEGIS <span class="dim">SECURE</span></h1>
            <p>TERMINAL_ACCESS_POINT</p>
          </div>
        </div>
        <div class="auth-divider"></div>
      </div>

      <form @submit.prevent="handleLogin" class="auth-form">
        <div class="auth-input-group">
          <label for="id">OPERATOR_ID</label>
          <input 
            type="text" 
            id="id" 
            v-model="subjectId" 
            placeholder="[ID_0000]" 
            spellcheck="false"
            required
          />
        </div>

        <div class="auth-input-group">
          <label for="token">ACCESS_KEY</label>
          <input 
            type="password" 
            id="token" 
            v-model="token" 
            placeholder="********" 
            required
          />
        </div>

        <div v-if="error" class="auth-error">
          &gt; ERROR: {{ error.toUpperCase() }}
        </div>

        <button type="submit" class="auth-btn" :disabled="loading">
          {{ loading ? 'ENCRYPTING...' : 'INITIALIZE_AUTH' }}
        </button>
      </form>

      <div class="auth-footer">
        <div class="status-box">
          <span class="status-dot"></span>
          <span>NODE_CONNECTED: 2.152.0.1</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router'; // 1. Импортируем useRouter
const subjectId = ref('');
const token = ref('');
const loading = ref(false);
const error = ref('');

const router = useRouter()

const handleLogin = async () => {
  loading.value = true;
  error.value = '';
  
  try {
    const response = await fetch('http://localhost:8000/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: subjectId.value, password: token.value })
    });

    if (!response.ok) throw new Error("Invalid credentials.");

    const data = await response.json();
    
    // Store token for later use
    localStorage.setItem('user-token', data.token);
    
    // Redirect to dashboard
    router.push('/'); 
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.auth-container {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--s-bg);
  font-family: var(--font-mono);
  color: var(--s-white);
}

.auth-box {
  width: 400px;
  background: var(--s-bg2);
  padding: 48px;
  border: 1px solid var(--s-line);
  border-bottom: 2px solid var(--s-line2);
}

.auth-header {
  margin-bottom: 40px;
}

.auth-logo {
  display: flex;
  align-items: center;
  gap: 16px;
  color: var(--s-white);
}

.logo-text h1 {
  font-size: 1.25rem;
  font-family: var(--font-sans);
  font-weight: 700;
  letter-spacing: 0.1em;
  margin: 0;
  line-height: 1;
}

.logo-text h1 .dim {
  color: var(--s-dim);
  font-weight: 400;
}

.logo-text p {
  font-size: 10px;
  color: var(--s-dim);
  margin-top: 4px;
  letter-spacing: 0.2em;
}

.auth-divider {
  height: 1px;
  background: var(--s-line);
  margin-top: 24px;
  position: relative;
}

.auth-divider::after {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  width: 40px;
  height: 1px;
  background: var(--s-line2);
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.auth-input-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.auth-input-group label {
  font-size: 10px;
  font-weight: 600;
  color: var(--s-mid);
  letter-spacing: 0.1em;
}

.auth-input-group input {
  width: 100%;
  padding: 12px;
  background: var(--s-bg);
  border: 1px solid var(--s-line);
  color: var(--s-white);
  font-family: var(--font-mono);
  font-size: 13px;
  outline: none;
  transition: all 0.2s ease;
}

.auth-input-group input:focus {
  border-color: var(--s-mid);
  background: var(--s-bg3);
}

.auth-input-group input::placeholder {
  color: var(--s-dim);
}

.auth-error {
  color: var(--s-err);
  font-size: 11px;
  padding: 8px;
  border-left: 2px solid var(--s-err);
  background: rgba(122, 58, 58, 0.05);
}

.auth-btn {
  width: 100%;
  padding: 14px;
  background: var(--s-bg4);
  border: 1px solid var(--s-line2);
  color: var(--s-white);
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  letter-spacing: 0.1em;
  transition: all 0.2s ease;
}

.auth-btn:hover {
  background: var(--s-bg3);
  border-color: var(--s-white);
}

.auth-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.auth-footer {
  margin-top: 40px;
  padding-top: 24px;
  border-top: 1px solid var(--s-line);
}

.status-box {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 9px;
  color: var(--s-dim);
  letter-spacing: 0.1em;
}

.status-dot {
  width: 4px;
  height: 4px;
  background: var(--s-ok);
}
</style>