<template>
  <div class="hero">
    <h2>Welcome to Vehicle Service Portal</h2>
    <p>Manage your vehicle maintenance, search available service packages, and track status easily using Vue 3.</p>
    <RouterLink to="/courses" className="btn">Explore Services</RouterLink>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router';
</script>

<style scoped>
.hero {
  background-color: #ffffff;
  padding: 3rem;
  border-radius: 8px;
  text-align: center;
  border: 1px solid #e2e8f0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

h2 {
  font-size: 2rem;
  color: #0f172a;
  margin-bottom: 1rem;
}

p {
  color: #64748b;
  max-width: 600px;
  margin: 0 auto 1.5rem auto;
}

.btn {
  display: inline-block;
  background-color: #2563eb;
  color: #ffffff;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 600;
}

.btn:hover {
  background-color: #1d4ed8;
}
</style>
