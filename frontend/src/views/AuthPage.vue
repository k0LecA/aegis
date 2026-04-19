<template>
  <div class="aperture-container">
    <div class="login-box">
      <div class="logo">
        <div class="aperture-circle"></div>
        <h1>APERTURE <span class="thin">SCIENCE</span></h1>
      </div>

      <div class="form-header">
        <p>Laboratories Personnel Portal</p>
        <div class="divider"></div>
      </div>

      <form @submit.prevent="handleLogin">
        <div class="input-group">
          <label for="id">SUBJECT ID</label>
          <input 
            type="text" 
            id="id" 
            v-model="subjectId" 
            placeholder="[REDACTED]" 
            required
          />
        </div>

        <div class="input-group">
          <label for="token">ACCESS TOKEN</label>
          <input 
            type="password" 
            id="token" 
            v-model="token" 
            placeholder="••••••••" 
            required
          />
        </div>

        <div v-if="error" class="error-msg">
          {{ error }}
        </div>

        <button type="submit" :disabled="loading">
          {{ loading ? 'INITIALIZING...' : 'BEGIN TESTING' }}
        </button>
      </form>

      <div class="footer-note">
        "We do what we must because we can."
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
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

.aperture-container {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f0f0f0;
  font-family: 'Roboto', sans-serif;
  color: #333;
}

.login-box {
  width: 350px;
  background: white;
  padding: 40px;
  border: 1px solid #ccc;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}

.logo {
  text-align: center;
  margin-bottom: 30px;
}

.aperture-circle {
  width: 60px;
  height: 60px;
  border: 8px solid #333;
  border-radius: 50%;
  margin: 0 auto 10px;
  position: relative;
  /* Simple CSS representation of the aperture blades */
  background: conic-gradient(
    from 0deg,
    #fff 0deg 45deg,
    #333 45deg 46deg,
    #fff 46deg 90deg,
    #333 90deg 91deg,
    #fff 91deg 135deg,
    #333 135deg 136deg,
    #fff 136deg 180deg,
    #333 180deg 181deg,
    #fff 181deg 225deg,
    #333 225deg 226deg,
    #fff 226deg 270deg,
    #333 270deg 271deg,
    #fff 271deg 315deg,
    #333 315deg 316deg,
    #fff 316deg 360deg
  );
}

h1 {
  font-size: 1.2rem;
  letter-spacing: 2px;
  margin: 0;
}

.thin { font-weight: 300; }

.form-header {
  margin-bottom: 25px;
}

.form-header p {
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  margin-bottom: 5px;
  color: #666;
}

.divider {
  height: 4px;
  background-color: #ff9d00; /* Aperture Orange */
  width: 40px;
}

.input-group {
  margin-bottom: 20px;
}

label {
  display: block;
  font-size: 0.7rem;
  font-weight: 700;
  margin-bottom: 5px;
}

input {
  width: 100%;
  padding: 10px;
  border: 2px solid #ddd;
  background-color: #fcfcfc;
  font-family: monospace;
  box-sizing: border-box;
  outline: none;
  transition: border-color 0.2s;
}

input:focus {
  border-color: #0094ff; /* Aperture Blue */
}

button {
  width: 100%;
  padding: 12px;
  background-color: #333;
  color: white;
  border: none;
  font-weight: 700;
  cursor: pointer;
  letter-spacing: 1px;
  transition: background-color 0.2s;
}

button:hover {
  background-color: #ff9d00;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.error-msg {
  color: #d00;
  font-size: 0.75rem;
  margin-bottom: 15px;
  font-style: italic;
}

.footer-note {
  margin-top: 30px;
  font-size: 0.7rem;
  color: #999;
  text-align: center;
}
</style>