<template>
  <div>
    <h2>Vehicle Owner Profile & Summary</h2>

    <div class="summary-card">
      <p><strong>Owner:</strong> John Doe</p>
      <p><strong>Email:</strong> john.doe@vehicleservice.com</p>
      <p><strong>Total Enrolled Credits/Hours:</strong> {{ store.totalCredits }}</p>
    </div>

    <h3 class="section-title">Booked Services</h3>
    <div v-if="store.enrolledCourses.length === 0" class="empty-text">
      No services enrolled currently.
    </div>

    <ul v-else class="enrolled-list">
      <li v-for="item in store.enrolledCourses" :key="item.id" class="enrolled-item">
        <div>
          <strong>{{ item.code }} — {{ item.name }}</strong> ({{ item.credits }} Credits)
        </div>
        <button class="btn-remove" @click="store.unenroll(item.id)">
          Cancel Booking
        </button>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { useEnrollmentStore } from '../stores/enrollment';

const store = useEnrollmentStore();
</script>

<style scoped>
.summary-card {
  background-color: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 1.5rem;
  margin-top: 1rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.section-title {
  margin-top: 2rem;
  color: #0f172a;
}

.empty-text {
  color: #64748b;
  margin-top: 0.5rem;
}

.enrolled-list {
  list-style: none;
  margin-top: 1rem;
}

.enrolled-item {
  background-color: #ffffff;
  border: 1px solid #e2e8f0;
  padding: 1rem 1.5rem;
  border-radius: 6px;
  margin-bottom: 0.75rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.btn-remove {
  background-color: #dc2626;
  color: #ffffff;
  border: none;
  padding: 0.4rem 0.8rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
}

.btn-remove:hover {
  background-color: #b91c1c;
}
</style>
