import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { environment } from '../../../environments/environment';

interface User {
  id: number;
  email: string;
  avatar?: string;
  role: string;
}

interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private readonly TOKEN_KEY = 'token';
  private readonly USER_KEY = 'user';
  private readonly isAuthenticatedSubject = new BehaviorSubject<boolean>(this.hasToken());
  private currentUser: User | null = null;

  readonly isAuthenticated$ = this.isAuthenticatedSubject.asObservable();

  constructor(private http: HttpClient) {
    // Initialize current user from localStorage if exists
    this.loadUserFromStorage();
  }

  private loadUserFromStorage(): void {
    try {
      const userStr = localStorage.getItem(this.USER_KEY);
      if (userStr) {
        this.currentUser = JSON.parse(userStr);
      }
    } catch (error) {
      console.error('Error loading user from storage:', error);
      this.currentUser = null;
    }
  }

  isAuthenticated(): boolean {
    return this.hasToken();
  }

  getCurrentUser(): User | null {
    return this.currentUser;
  }

  private hasToken(): boolean {
    return !!localStorage.getItem(this.TOKEN_KEY);
  }

  login(credentials: { email: string; password: string }): Observable<LoginResponse> {
    const formData = new FormData();
    formData.append('username', credentials.email);
    formData.append('password', credentials.password);

    return this.http.post<LoginResponse>(`${environment.apiUrl}/token`, formData)
      .pipe(
        tap(response => {
          localStorage.setItem(this.TOKEN_KEY, response.access_token);
          localStorage.setItem(this.USER_KEY, JSON.stringify(response.user));
          this.currentUser = response.user;
          this.isAuthenticatedSubject.next(true);
        })
      );
  }

  logout(): void {
    localStorage.removeItem(this.TOKEN_KEY);
    localStorage.removeItem(this.USER_KEY);
    this.isAuthenticatedSubject.next(false);
  }
}
