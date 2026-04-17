theory Proseminar

imports Main

begin

lemma neco: "(A \<longrightarrow> B) \<longrightarrow> (\<not>B \<longrightarrow> \<not>A)"
proof
  assume ab: "A \<longrightarrow> B"
  show "\<not>B \<longrightarrow> \<not>A"
  proof
    assume nb: "\<not>B"
    show "\<not>A"
    proof
      assume a: "A"
      from ab and a have b: "B"
        by simp
      
      from nb and b show False
        by simp
      


end