/**
 * A tiny localStorage-backed store for useSyncExternalStore.
 *
 * Every read and write is wrapped: private windows and blocked storage simply
 * fall back to defaults, and the page keeps working.
 */

type Listener = () => void;

export type Store<T> = {
  get: () => T;
  getServer: () => T;
  set: (next: T | ((previous: T) => T)) => void;
  subscribe: (listener: Listener) => () => void;
};

export function createStore<T>(read: () => T, write: (value: T) => void, fallback: T): Store<T> {
  let cache: T | undefined;
  const listeners = new Set<Listener>();

  const get = (): T => {
    if (cache === undefined) {
      try {
        cache = typeof window === "undefined" ? fallback : read();
      } catch {
        cache = fallback;
      }
    }
    return cache;
  };

  return {
    get,
    getServer: () => fallback,
    set(next) {
      cache = typeof next === "function" ? (next as (previous: T) => T)(get()) : next;
      try {
        write(cache);
      } catch {
        // Storage is full or blocked; the value still lives for this page.
      }
      listeners.forEach((listener) => listener());
    },
    subscribe(listener) {
      listeners.add(listener);
      const onStorage = (event: StorageEvent) => {
        if (event.key === null || event.key.startsWith("sat-")) {
          cache = undefined;
          listener();
        }
      };
      window.addEventListener("storage", onStorage);
      return () => {
        listeners.delete(listener);
        window.removeEventListener("storage", onStorage);
      };
    },
  };
}

export function readItem(key: string): string | null {
  try {
    return window.localStorage.getItem(key);
  } catch {
    return null;
  }
}

export function writeItem(key: string, value: string): void {
  try {
    window.localStorage.setItem(key, value);
  } catch {
    // ignore
  }
}
