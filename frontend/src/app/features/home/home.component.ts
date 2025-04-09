import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

interface Activity {
  id: number;
  name: string;
  imageUrl: string;
  description: string;
}

interface Award {
  id: number;
  name: string;
  imageUrl: string;
  description: string;
}

interface VolunteerWork {
  name: string;
  description: string;
  period: string;
  imageUrl: string;
}

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {
  constructor(private router: Router) {}

  selectedActivity: Activity | null = null;
  selectedAward: Award | null = null;

  activities: Activity[] = [
    {
      id: 1,
      name: 'Debate Team',
      imageUrl: 'https://cdn.usegalileo.ai/sdxl10/bd87f91f-8b5f-4964-bf74-b62f84fe0427.png',
      description: 'Lead speaker in the school debate team, participating in regional competitions.'
    },
    {
      id: 2,
      name: 'Student Council',
      imageUrl: 'https://cdn.usegalileo.ai/sdxl10/f039741a-3105-4370-b69c-84d6d4e64000.png',
      description: 'Serving as Student Body President, organizing school events and representing student interests.'
    },
    {
      id: 3,
      name: 'Environmental Club',
      imageUrl: 'https://cdn.usegalileo.ai/sdxl10/12ad004f-190a-4fc4-8699-2217795f4f85.png',
      description: 'Leading initiatives for campus sustainability and environmental awareness.'
    },
    {
      id: 4,
      name: 'Model United Nations',
      imageUrl: 'https://cdn.usegalileo.ai/sdxl10/6ce5a165-61cc-4b15-85a6-93d1310e3230.png',
      description: 'Representing countries in simulated UN conferences and diplomatic negotiations.'
    },
    {
      id: 5,
      name: 'Robotics Club',
      imageUrl: 'https://cdn.usegalileo.ai/sdxl10/75e8f92b-78e3-43bd-a38b-6311742abf7e.png',
      description: 'Building and programming robots for regional competitions.'
    },
    {
      id: 6,
      name: 'School Newsletter',
      imageUrl: 'https://cdn.usegalileo.ai/sdxl10/f553338f-baa8-4f43-9dfd-26f0d2064562.png',
      description: 'Editor-in-chief of the school newspaper, managing content and team of writers.'
    },
    {
      id: 7,
      name: 'Math Team',
      imageUrl: 'https://cdn.usegalileo.ai/sdxl10/c5bd7ef8-4a82-49ed-af72-a507b6570460.png',
      description: 'Competing in mathematics competitions at state and national levels.'
    },
    {
      id: 8,
      name: 'Drama Club',
      imageUrl: 'https://cdn.usegalileo.ai/sdxl10/1e593cd0-d320-439f-8c17-5328cd508071.png',
      description: 'Lead roles in school productions and theater workshops.'
    },
    {
      id: 9,
      name: 'Science Olympiad',
      imageUrl: 'https://cdn.usegalileo.ai/sdxl10/8e9b9a80-9b15-424a-9f1e-563a196b892a.png',
      description: 'Participating in various science competitions and research projects.'
    },
    {
      id: 10,
      name: 'Language Club',
      imageUrl: 'https://cdn.usegalileo.ai/sdxl10/d8be5d22-d4c9-4665-bafe-0c2ef6aa677f.png',
      description: 'Organizing cultural events and language exchange programs.'
    }
  ];

  awards: Award[] = [
    {
      id: 1,
      name: 'National Merit Scholarship',
      imageUrl: 'https://cdn.usegalileo.ai/sdxl10/6cbbfe74-9ecb-484f-a5b7-8247dfbbb50c.png',
      description: 'Awarded for outstanding academic achievement and test scores.'
    },
    {
      id: 2,
      name: 'Presidential Service Award',
      imageUrl: 'https://cdn.usegalileo.ai/sdxl10/8e9b9a80-9b15-424a-9f1e-563a196b892a.png',
      description: 'Recognition for 100+ hours of community service.'
    },
    {
      id: 3,
      name: 'Science Fair Gold Medal',
      imageUrl: 'https://cdn.usegalileo.ai/sdxl10/bd87f91f-8b5f-4964-bf74-b62f84fe0427.png',
      description: 'First place in State Science Fair for innovative research project.'
    },
    {
      id: 4,
      name: 'Outstanding Leadership Award',
      imageUrl: 'https://cdn.usegalileo.ai/sdxl10/f039741a-3105-4370-b69c-84d6d4e64000.png',
      description: 'Recognition for exceptional leadership in student government.'
    },
    {
      id: 5,
      name: 'Math Competition Winner',
      imageUrl: 'https://cdn.usegalileo.ai/sdxl10/12ad004f-190a-4fc4-8699-2217795f4f85.png',
      description: 'First place in State Mathematics Competition.'
    },
    {
      id: 6,
      name: 'Best Delegate Award',
      imageUrl: 'https://cdn.usegalileo.ai/sdxl10/6ce5a165-61cc-4b15-85a6-93d1310e3230.png',
      description: 'Outstanding performance at Model United Nations conference.'
    },
    {
      id: 7,
      name: 'Environmental Stewardship',
      imageUrl: 'https://cdn.usegalileo.ai/sdxl10/75e8f92b-78e3-43bd-a38b-6311742abf7e.png',
      description: 'Recognition for leading school sustainability initiatives.'
    },
    {
      id: 8,
      name: 'Robotics Competition Winner',
      imageUrl: 'https://cdn.usegalileo.ai/sdxl10/f553338f-baa8-4f43-9dfd-26f0d2064562.png',
      description: 'First place in Regional Robotics Championship.'
    },
    {
      id: 9,
      name: 'Excellence in Journalism',
      imageUrl: 'https://cdn.usegalileo.ai/sdxl10/c5bd7ef8-4a82-49ed-af72-a507b6570460.png',
      description: 'State award for outstanding school newspaper editorship.'
    },
    {
      id: 10,
      name: 'Performing Arts Achievement',
      imageUrl: 'https://cdn.usegalileo.ai/sdxl10/1e593cd0-d320-439f-8c17-5328cd508071.png',
      description: 'Recognition for outstanding contributions to school theater.'
    }
  ];

  showActivityDetails(activity: Activity, event: Event) {
    event.stopPropagation();
    this.selectedActivity = this.selectedActivity?.id === activity.id ? null : activity;
  }

  showAwardDetails(award: Award, event: Event) {
    event.preventDefault();
    this.selectedAward = award;
  }

  navigateToActivity(id: number, event: Event) {
    event.stopPropagation();
    this.router.navigate(['/activities', id]);
  }

  navigateToAward(id: number) {
    this.router.navigate(['/awards', id]);
  }

  closePopup() {
    this.selectedActivity = null;
  }
}
