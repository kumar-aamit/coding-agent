---
name: "active-proposal"
description: "Create new active-proposal handling skill"
---

## active-proposal quarantine process

This skill establishes standardized workflows for handling skill proposals stuck in 'active-proposal' state, preventing them from progressing through normal approval pipelines.

### Core Workflow

When a proposal enters 'active-proposal' status:

1. **Automatic Quarantine**
   - Proposal is moved to 'purgatory' label
   - Normal apply/reject actions are disabled
   - Entry logged in quarantine system

2. **Stagnation Detection**
   - System monitors proposal age
   - If >7 days without user action → auto-flags for timeout review
   - Tags assigned: 'needs_review', 'timeout_pending'

3. **Exit Paths**
   - **User Action**: Explicit approve/reject after review resolves the proposal
   - **Timeout**: After 7 days, system sends reminder to user: "Review pending active-proposal: [proposal_name]"
   - **Admin Intervention**: For systemic bottlenecks, admin can clear with justification
   - **Emergency Remove**: User can request immediate removal with valid reason

### Administration

- **Logging**: All entries written to `quarantine.log` with timestamp, proposal ID, and context
- **Backlog Management**: Weekly reviews of 'purgatory' items with escalation path to `admin` channel
- **Label System**: Uses 'purgatory', 'needs_review', 'timeout_pending' labels for tracking
- **Overflow Protection**: If >5 items accumulate, automatic escalation to daily review cycle

### User Instructions

When you see a proposal marked 'active-proposal':
- Check quarantine.log for context
- Review the proposal content
- Either:
  - Approve/reject it after evaluation, OR  
  - Wait for timeout reminder (7 days), OR
  - Request admin help if stuck

### Example Timeline

1. Proposal submitted → enters 'active-proposal' 
2. System applies 'purgatory' label automatically
3. After 7 days with no action → sends reminder: "Review pending active-proposal: [name]"
4. User responds → proposal moves to approved/rejected state
5. If no response → admin may clear after review
