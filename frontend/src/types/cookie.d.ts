// frontend/src/types/cookie.d.ts
declare module 'js-cookie' {
  interface CookieAttributes {
    expires?: number | Date;
    path?: string;
    domain?: string;
    secure?: boolean;
    sameSite?: 'strict' | 'lax' | 'none';
  }

  const cookie: {
    set(name: string, value: string, options?: CookieAttributes): void;
    get(name: string): string | undefined;
    remove(name: string, options?: CookieAttributes): void;
    getJSON<T>(name: string): T | undefined;
  };

  export default cookie;
}