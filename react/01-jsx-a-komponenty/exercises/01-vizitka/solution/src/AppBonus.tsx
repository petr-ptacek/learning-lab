import { ContactInfo, ProfileCard } from "./ProfileCardBonus.tsx";

export default function () {
  return (
    <div>
      <ProfileCard name="Petr Ptacek" role="Frontend Developer">
        <ContactInfo email="petr.ptacek99@gmail.com" />
      </ProfileCard>
    </div>
  );
}