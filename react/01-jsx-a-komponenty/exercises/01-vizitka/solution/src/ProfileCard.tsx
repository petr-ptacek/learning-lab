export interface ProfileCardProps {
  name: string;
  role: string;
  email: string;
}

export function ProfileCard(props: ProfileCardProps) {
  return (
    <div style={ { display: "inline-block", } }>
      <span>{ props.name }</span> | <span>{ props.role }</span> | <span>{ props.email } </span>
    </div>
  );
}