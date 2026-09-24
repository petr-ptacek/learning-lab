import type React from "react";

export function ContactInfo({ email }: { email: string }) {
  return (
    <div>{ email }</div>
  );
}

interface ProfileCardProps {
  name: string;
  role: string;
  children: React.ReactNode;
}

export function ProfileCard({ name, role, children }: ProfileCardProps) {
  return (
    <div>
      <p>{ name }</p>
      <p>{ role }</p>
      { children }
    </div>
  );
}
