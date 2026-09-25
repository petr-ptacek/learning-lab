import * as React from "react";

interface AlertProps {
  children: React.ReactNode;
  icon: React.ReactNode;
}

export function Alert(props: AlertProps) {
  return (
    <div>
      <span>{ props.icon }</span>&nbsp;<span>{ props.children }</span>
    </div>
  );
}