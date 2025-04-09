import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

type AwardCategory = 'all' | 'academic' | 'extracurricular' | 'service';

interface Award {
  id: number;
  title: string;
  organization: string;
  date: string;
  description: string;
  imageUrl: string;
  category: Exclude<AwardCategory, 'all'>;
}

@Component({
  selector: 'app-awards',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './awards.component.html'
})
export class AwardsComponent {
  categories: AwardCategory[] = ['all', 'academic', 'extracurricular', 'service'];
  selectedCategory: AwardCategory = 'all';

  awards: Award[] = [
    {
      id: 1,
      title: 'First Place - Science Fair',
      organization: 'National Science Foundation',
      date: '2024',
      description: 'Awarded first place for research project on renewable energy solutions',
      imageUrl: 'https://cdn.usegalileo.ai/sdxl10/6cbbfe74-9ecb-484f-a5b7-8247dfbbb50c.png',
      category: 'academic'
    },
    {
      id: 2,
      title: 'Leadership Excellence Award',
      organization: 'Student Council',
      date: '2023',
      description: 'Recognized for outstanding leadership in student government',
      imageUrl: 'https://cdn.usegalileo.ai/sdxl10/8e9b9a80-9b15-424a-9f1e-563a196b892a.png',
      category: 'extracurricular'
    },
    {
      id: 3,
      title: 'Community Service Award',
      organization: 'Local Youth Foundation',
      date: '2023',
      description: '100+ hours of community service',
      imageUrl: 'https://cdn.usegalileo.ai/sdxl10/d8be5d22-d4c9-4665-bafe-0c2ef6aa677f.png',
      category: 'service'
    }
  ];

  filterAwards(category: AwardCategory) {
    this.selectedCategory = category;
  }

  get filteredAwards() {
    return this.selectedCategory === 'all'
      ? this.awards
      : this.awards.filter(award => award.category === this.selectedCategory);
  }
}
