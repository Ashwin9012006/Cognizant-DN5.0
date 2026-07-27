<template>
  <div class="detail-card">
    <div class="code">{{ course?.code }}</div>
    <h2>{{ course?.name }}</h2>
    <p>Complete professional maintenance package detailing fluid, electrical, and physical inspections.</p>

    <div class="meta">
      <p><strong>Credits / Hours:</strong> {{ course?.credits }}</p>
      <p><strong>Status / Grade:</strong> {{ course?.grade }}</p>
    </div>

    <div class="actions">
      <button
        class="btn-primary"
        :disabled="isEnrolled"
        @click="handleEnroll"
      >
        {{ isEnrolled ? 'Enrolled' : 'Enroll & View Profile' }}
      </button>
      <RouterLink to="/courses" class="btn-secondary">Back to List</RouterLink>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute, useRouter, RouterLink } from 'vue-router';
import { useEnrollmentStore } from '../stores/enrollment';

const route = useRoute();
const router = useRouter();
const store = useEnrollmentStore();

const allCourses = [
  { id: 1, name: "Engine Oil & Filter Change", code: "VS101", credits: 4, grade: "Completed (A)" },
  { id: 2, name: "Brake System Inspection", code: "VS102", credits: 3, grade: "Verified (A)" },
  { id: 3, name: "Wheel Alignment & Balancing", code: "VS103", credits: 5, grade: "Scheduled (B)" },
  { id: 4, name: "Transmission Flush & Service", code: "VS104", credits: 4, grade: "Completed (A)" },
  { id: 5, name: "Battery & Electrical Audit", code: "VS105", credits: 2, grade: "Verified (A)" }
];

const courseId = computed(() => parseInt(route.params.id, 10));
const course = computed(() => allCourses.find(c => c.id === courseId.value));

const isEnrolled = computed(() => {
  return course.value && store.enrolledCourses.some(c => c.id === course.value.id);
});

const handleEnroll = () => {
  if (course.value) {
    store.enroll(course.value);
    router.push('/profile'); // Programmatic navigation to /profile
  }
};
</script>

<style scoped>
.detail-card {
  background-color: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.code {
  color: #64748b;
  font-size: 0.85rem;
}

h2 {
  color: #0f172a;
  margin-bottom: 0.5rem;
}

.meta {
  margin: 1.5rem 0;
  background: #f1f5f9;
  padding: 1rem;
  border-radius: 6px;
}

.actions {
  display: flex;
  gap: 1rem;
}

.btn-primary {
  background-color: #2563eb;
  color: #ffffff;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
}

.btn-primary:disabled {
  background-color: #94a3b8;
  cursor: not-allowed;
}

.btn-secondary {
  background-color: #64748b;
  color: #ffffff;
  padding: 0.6rem 1.2rem;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 600;
}
</style>
