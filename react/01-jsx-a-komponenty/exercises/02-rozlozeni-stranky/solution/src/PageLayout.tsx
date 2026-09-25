import * as React from "react";

interface PageLayoutProps {
  header: React.ReactNode;
  children: React.ReactNode;
  footer: React.ReactNode;
}

export function PageLayout(props: PageLayoutProps) {
  return (
    <div>
      <header>
        { props.header }
      </header>
      <main>
        { props.children }
      </main>
      <footer>
        { props.footer }
      </footer>
    </div>
  );
}