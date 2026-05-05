# =============================================================================
# Gherkin spec for this slice. WRITE THIS FILE FIRST — before any client/api/db
# code. Implementation is complete only when every scenario passes.
#
# Numbering convention: every Given/When/Then line ends with `# Step N/M` so
# step output, Sentry spans, and review comments can reference exact steps.
# Keep step phrasing identical to the matching definition in steps/.
# =============================================================================

Feature: {slice-name}
  As a {role}
  I want to {capability}
  So that {business-outcome}

  Background:
    Given the feature flag "{slice_name}_v2" is enabled            # Step 0/M
    And the user is authenticated                                  # Step 0/M

  Scenario: {happy-path-scenario-name}
    Given {precondition}                                           # Step 1/M
    And {additional-precondition}                                  # Step 2/M
    When {user-action}                                             # Step 3/M
    Then {observable-outcome}                                      # Step 4/M
    And a Sentry breadcrumb is recorded with slice="{slice-name}"  # Step 5/M

  Scenario: {error-path-scenario-name}
    Given {precondition}                                           # Step 1/M
    When {failing-action}                                          # Step 2/M
    Then the error is captured via withSliceContext()              # Step 3/M
    And the user sees {graceful-error-state}                       # Step 4/M

# -----------------------------------------------------------------------------
# Authoring notes (delete once the feature is fleshed out):
#   - One Feature per slice. Multiple Scenarios are fine; keep them focused.
#   - Replace every {placeholder} before this file is committed.
#   - Step text must be identical between this file and steps/{slice-name}.steps.{EXT}.
#   - Each Scenario is one Sentry trace end-to-end (Article 20e-2).
#   - The .feature file is the QA gate. Slice ships when all scenarios pass.
# -----------------------------------------------------------------------------
