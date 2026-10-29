#!/usr/bin/env python3
"""
CaseZero — Terminal / CLI Edition.
Reuses the exact same Python DSA packages:
- dsa.hashmap.CustomHashMap
- dsa.graph.SuspectGraph
- dsa.sets_engine.SuspectSetEngine
- dsa.tree.InvestigationTree
- dsa.search.TimelineBinarySearch & EvidenceTrie
- game.state.GameSession
"""

import sys
from game.state import GameSession

def print_banner():
    print("\n" + "=" * 65)
    print("  CASEZERO — ALGORITHMIC FORENSIC INVESTIGATION (CLI)")
    print("  Powered by Data Structures & Algorithms")
    print("=" * 65)

def main():
    print_banner()
    session = GameSession()
    session.start_case("case_1")

    print(f"\n[ACTIVE DOSSIER] {session.case_data['title']} ({session.case_data['location']})")
    print(f"Briefing: {session.case_data['briefing']}\n")

    while True:
        state = session.to_dict()
        viable_count = len(state['viable_suspect_ids'])
        print(f"\n--- STATUS: [AP: {session.ap}/12] | [Viable Suspects: {viable_count}] | [Clues: {len(session.discovered_clues)}] ---")

        if state["contradiction_detected"]:
            print("\n🚨 CRITICAL CONTRADICTION: Viable pool is ∅! Two clues conflict.")
            print(f"Conflicting clues: {state['conflicting_clues']}")

        print("1. Review Suspects (HashMap O(1))")
        print("2. Suspect Network & Collusion Path (Graph BFS)")
        print("3. Explore Leads (Decision Tree)")
        print("4. Evidence & Set Theory (Venn Intersection)")
        print("5. Verify Alibi (Timeline Binary Search)")
        print("6. Debunk Forgery Clue")
        print("7. Issue Arrest Warrant (Accusation)")
        print("8. Exit")

        choice = input("\nSelect Action (1-8): ").strip()

        if choice == '1':
            print("\n--- SUSPECT DOSSIERS ---")
            for s in state["suspects"]:
                status = "VIABLE" if s["is_viable"] else "CLEARED"
                print(f"[{s['id']}] {s['name']:<18} | {s['role']:<24} | {status} | Traits: {', '.join(s['traits'])}")

        elif choice == '2':
            print("\n--- SUSPECT RELATIONSHIP NETWORK ---")
            for s_id, edges in session.graph.adj.items():
                s_name = session.suspect_map.get(s_id)['name']
                edge_strs = [f"-> {e['target']} ({e['type']})" for e in edges if not e['debunked']]
                print(f"[{s_id}] {s_name:<18}: {', '.join(edge_strs) if edge_strs else 'None'}")

            sub = input("\nFind BFS Collusion Path? (Enter start and target, e.g. 'S1 S6' or press Enter to return): ").strip().split()
            if len(sub) == 2:
                res = session.query_path(sub[0].upper(), sub[1].upper())
                if res.get("found"):
                    print(f"✓ Shortest Path ({len(res['path'])} nodes): {' -> '.join(res['path'])}")
                else:
                    print("No connection path found.")

        elif choice == '3':
            print("\n--- INVESTIGATION DECISION TREE ---")
            pre = session.tree.pre_order_traversal()
            for idx, n in enumerate(pre, 1):
                sym = "✓" if n["status"] == "RESOLVED" else ("⚡" if n["status"] == "AVAILABLE" else "🔒")
                print(f"[{sym}] #{idx} [{n['id']}] {n['title']:<28} | Category: {n['category']:<12} | Cost: {n['ap_cost']} AP | {n['status']}")

            lead_id = input("\nEnter Lead ID to investigate (or Enter to cancel): ").strip().upper()
            if lead_id:
                res = session.explore_lead(lead_id)
                print(res["message"])
                for c in res.get("new_clues", []):
                    print(f"  🔍 NEW CLUE DISCOVERED: [{c['id']}] {c['title']} - {c['desc']}")

        elif choice == '4':
            print("\n--- SET THEORY & EVIDENCE ---")
            for step in state["set_steps"]:
                print(f"  {step}")
            print(f"\nCurrent Viable Suspects: {state['viable_suspect_ids'] or '∅ (EMPTY SET)'}")
            print("\nCollected Clues:")
            for c in state["discovered_clues"]:
                forged_str = " [FORGERY DEBUNKED]" if c["debunked"] else ""
                print(f"  [{c['id']}] {c['title']}{forged_str}: {c['desc']} (Points to: {', '.join(c['allowed'])})")

        elif choice == '5':
            print("\n--- TIMELINE BINARY SEARCH ---")
            print("Access Logs:")
            for idx, log in enumerate(state["security_logs"]):
                print(f"  [{idx}] {log['time']} | {log['suspect_id']} | {log['event']} (@ {log['location']})")

            s_id = input("\nEnter Suspect ID to verify (e.g. S5): ").strip().upper()
            target_time = input("Enter Timestamp (e.g. 23:45): ").strip() or "23:45"
            if s_id:
                res = session.check_alibi(s_id, target_time)
                print("\nBinary Search Trace:")
                for step in res["trace"]["steps"]:
                    print(f"  Step {step['step']}: Low={step['low']}, Mid={step['mid']}, High={step['high']} -> {step['mid_time']} ({step['comparison']})")
                print(f"\nResult: {res['summary']}")

        elif choice == '6':
            clue_id = input("\nEnter Clue ID to expose as forgery (e.g. C3): ").strip().upper()
            if clue_id:
                res = session.debunk_clue(clue_id)
                print(res["message"])

        elif choice == '7':
            culprit = input("\nEnter Prime Culprit Suspect ID (e.g. S4): ").strip().upper()
            accomplice = input("Enter Inside Accomplice Suspect ID (or Enter if none): ").strip().upper()
            verdict = session.submit_accusal(culprit, accomplice)
            print("\n" + "=" * 50)
            if verdict["is_solved"]:
                print("  🎉 CONVICTION SECURED! INDICTMENT SUCCESSFUL!")
            else:
                print("  ❌ CASE COLLAPSED: FALSE ARREST!")
            print(f"  Score: {verdict['score']} Pts | Detective Rank: {verdict['rank']}")
            print("=" * 50)
            break

        elif choice == '8':
            print("\nInvestigation suspended.")
            break

if __name__ == "__main__":
    main()
