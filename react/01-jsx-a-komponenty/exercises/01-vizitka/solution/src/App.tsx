import { ProfileCard } from "./ProfileCard";

type User = {
  name: string;
  role: string;
  email: string;
}


export default function App() {
  const users: User[] = [
    {
      name: "Petr Ptacek",
      role: "Frontend Developer",
      email: "petr@example.com"
    },
    {
      name: "Jana Nováková",
      role: "UX Designer",
      email: "jana.novakova@firma.cz"
    },
    {
      name: "Karel Svoboda",
      role: "Backend Developer",
      email: "karel@svoboda.dev"
    }
  ];

  const usersHtml = users.map(user =>
    (
      <div
        key={ user.name }
        style={ { border: "1px solid gray" } }
      >
        <ProfileCard name={ user.name } role={ user.role } email={ user.email } />
      </div>
    )
  );

  return (
    <div style={ { display: "flex", gap: "1rem", flexDirection: "column" } }>
      { usersHtml }
    </div>
  );
}