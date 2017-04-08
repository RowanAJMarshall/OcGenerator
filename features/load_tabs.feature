Feature: View generated tabs

  Scenario: Generated tabs
    Given I have selected the file ocarina.wav
    When I click on submit
    Then I see the tabs appear after 3 seconds