import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  template: `
    <app-header></app-header>
    <main class="main-content">
      <router-outlet></router-outlet>
    </main>
    <footer>
      <p>&copy; 2026 Vehicle Service Management System. All rights reserved.</p>
    </footer>
  `
})
export class AppComponent {
  title = 'student-portal-angular';
}
