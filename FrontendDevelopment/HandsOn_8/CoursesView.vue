<template>
  <div>
    <h2>Available Vehicle Maintenance Services</h2>

    <div class="controls">
      <input
        v-model="searchTerm"
        type="text"
        class="search-input"
        placeholder="Search services by name or code..."
      />
    </div>

    <div class="grid">
      <CourseCard
        v-for="course in filteredCourses"
        :key="course.id"
        :id="course.id"
        :name="course.name"
        :code="course.code"
        :credits="course.credits"
        :grade="course.grade"
        :is-enrolled="isEnrolled(course.id)"
        @enroll="handleEnroll(course)"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import CourseCard from '../components/CourseCard.vue';
import { useEnrollmentStore } from '../stores/enrollment';

const store = useEnrollmentStore();
const courses = ref([]);
const searchTerm = ref('');

onMounted(() => {
  courses.value = [
    { id: 1, name: "Engine Oil & Filter Change", code: "VS101", credits: 4, grade: "Completed (A)" },
    { id: 2, name: "Brake System Inspection", code: "VS102", credits: 3, grade: "Verified (A)" },
    { id: 3, name: "Wheel Alignment & Balancing", code: "VS103", credits: 5, grade: "Scheduled (B)" },
    { id: 4, name: "Transmission Flush & Service", code: "VS104", credits: 4, grade: "Completed (A)" },
    { id: 5, name: "Battery & Electrical Audit", code: "VS105", credits: 2, grade: "Verified (A)" }
  ];
});

const filteredCourses = computed(() => {
  const term = searchTerm.value.toLowerCase().trim();
  if (!term) return courses.value;
  return courses.value.filter(c =>
    c.name.toLowerCase().includes(term) || c.code.toLowerCase().includes(term)
  );
});

const isEnrolled = (courseId) => {
  return store.enrolledCourses.some(c => c.id === courseId);
};

const handleEnroll = (course) => {
  store.enroll(course);
};
</script>

<style scoped>
.controls {
  margin: 1.5rem 0;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}
</style>
