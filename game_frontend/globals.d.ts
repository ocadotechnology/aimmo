interface TriggerEvent {
  event: string;
}

interface DataLayer {
  push(event: TriggerEvent): void;
}

declare var dataLayer: number;
