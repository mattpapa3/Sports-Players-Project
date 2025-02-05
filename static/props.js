
$(document).ready(function() {
    $(".updateProps").off("click").on("click", function() {
        $(this).siblings(".updateProps").removeClass("button-selected");
        $(this).addClass("button-selected");
        var button = $(this);
        var parameter = $(this).data("parameter");
        var propsDiv = button.closest(".container").find(".propsDiv");
        var gameButton = document.querySelector('.gamescontainer .button-selected');
        if (gameButton) {
            // Do something with the selected button
            var parameter2 = gameButton.getAttribute('data-parameter');
            console.log('Selected Parameter:', parameter);
        } else {
            console.log('No button is selected in the gamescontainer.');
        }
        $.ajax({
            url: "/process",
            type: "POST",
            data: {parameter: parameter,
              parameter2: parameter2
             },
            success: function(response) {
                var updatedProps = "<table><thead>";
                updatedProps += "<tr> <th>Player</th> <th>Line</th> <th>PropCodes Score</th> <th>Views</th> <th>Over</th> <th>Under</th> <th>EV Over</th> <th> EV Under</th></tr></thead><tbody>";
                $.each(response.content, function(index, row){
                    updatedProps += "<tr>"
                    $.each(row, function(itemIndex, i) {
                        console.log(i)
                        if (itemIndex === 6)
                        {
                           updatedProps += ("<td>" + i + "</td>")
                        }
                        else if (itemIndex != 8 && itemIndex != 2 && itemIndex != 9 && itemIndex != 7)
                        {
                            updatedProps += ("<td>" + i + "</td>");
                        }
                    });
                    updatedProps += ("<td><button class='researchButton'");
                    $.each(row, function(itemIndex, i) {
                        console.log(i);
                        if (itemIndex === 0)
                        {
                            updatedProps += (" data-name='" + i + "'");
                        }
                        else if(itemIndex === 1)
                        {
                            updatedProps += (" data-line='" + i + "'");
                        }
                        else if (itemIndex === 2)
                        {
                            updatedProps += (" data-cat='" + i + "'");
                        }
                        else if(itemIndex == 8)
                        {
                          updatedProps += (" data-tot='" + i + "'")
                        }
                        else if(itemIndex == 9)
                        {
                          updatedProps += (" data-spread='" + i + "'")
                        }
                    });
                    updatedProps += ">Research</button></td></tr>";
                });
                updatedProps += "</tbody></table>"
                console.log(updatedProps)
                propsDiv.find("table").html(updatedProps);
            },
            error: function(error){
                console.log(error);
            }
        });
    });
});



$(document).ready(function() {
  $(".updateGame").off("click").on("click", function() {
      $(this).siblings(".updateGame").removeClass("button-selected");
      $(this).addClass("button-selected");
      var button = $(this);
      var parameter2 = $(this).data("parameter");
      //var propsDiv = button.closest(".container").find(".propsDiv");
      var propsDiv = $('.container .propsDiv');
      //var parameter = "k";
      var parameter = "points"
      console.log(parameter2);

      $.ajax({
          url: "/process",
          type: "POST",
          data: {parameter: parameter, parameter2: parameter2 },
          success: function(response) {
              var updatedProps = "<table><thead>";
              updatedProps += "<tr> <th>Player</th> <th>Line</th> <th>PropCodes Score</th> <th>Views</th> <th>Over</th> <th>Under</th> <th>EV Over</th> <th> EV Under</th></tr></thead><tbody>";
              $.each(response.content, function(index, row){
                  updatedProps += "<tr>"
                  $.each(row, function(itemIndex, i) {
                    console.log(i);
                      if (itemIndex === 6)
                      {
                         updatedProps += ("<td>" + i + "</td>")
                      }
                      else if (itemIndex != 2 && itemIndex != 8 && itemIndex != 9 && itemIndex != 7)
                      {
                          updatedProps += ("<td>" + i + "</td>");
                      }
                  });
                  updatedProps += ("<td><button class='researchButton'");
                  $.each(row, function(itemIndex, i) {
                      if (itemIndex === 0)
                      {
                          updatedProps += (" data-name='" + i + "'");
                      }
                      else if(itemIndex === 1)
                      {
                          updatedProps += (" data-line='" + i + "'");
                      }
                      else if (itemIndex === 2)
                      {
                          updatedProps += (" data-cat='" + i + "'");
                      }
                      else if(itemIndex == 8)
                      {
                        updatedProps += (" data-tot='" + i + "'");
                      }
                      else if(itemIndex == 9)
                      {
                        updatedProps += (" data-spread='" + i + "'");
                      }
                  });
                  updatedProps += ">Research</button></td></tr>";
              });
              updatedProps += "</tbody></table>"
              propsDiv.find("table").html(updatedProps);
          },
          error: function(error){
              console.log(error);
          }
      });
  });
});

$(document).ready(function() {
    $(".propsDiv").on("click", "table th", function() {
      var table = $(this).closest("table");
      var columnIndex = $(this).index();
      var rows = table.find("tbody > tr").get();
  
      rows.sort(function(a, b) {
        var aValue = $(a).find("td").eq(columnIndex).text();
        var bValue = $(b).find("td").eq(columnIndex).text();
  
        // Convert values to numbers if they are numeric
        var aNumeric = !isNaN(parseFloat(aValue)) && isFinite(aValue);
        var bNumeric = !isNaN(parseFloat(bValue)) && isFinite(bValue);
  
        if (aNumeric && bNumeric) {
          // If both values are numeric, compare as numbers in descending order
          return parseFloat(bValue) - parseFloat(aValue);
        } else if (aNumeric) {
          // If only aValue is numeric, aValue comes before bValue
          return -1;
        } else if (bNumeric) {
          // If only bValue is numeric, bValue comes before aValue
          return 1;
        } else {
          // If both values are non-numeric strings, compare as strings
          return aValue.localeCompare(bValue);
        }
      });
  
      $.each(rows, function(index, row) {
        table.append(row);
      });
    });
  });

$(document).ready(function() {
    $("#overButton, #underButton").off("click").on("click", function() {
        var button = $(this);
        var parameter1 = button.data("parameter1");
        var parameter2 = button.data("parameter2");
        var parameter3 = button.data("parameter3");
        var parameter4 = button.data("parameter4");
        var parameter5 = button.data("parameter5");
        var parameter6 = button.data("parameter6")

        $.ajax({
            url:"/voteOverUnder",
            type: "POST",
            data: {
                parameter1: parameter1,
                parameter2: parameter2,
                parameter3: parameter3,
                parameter4: parameter4,
                parameter5: parameter5,
                parameter6: parameter6
            },
            success: function(response) {

            },
            error: function(error) {
                console.log(error)
            }
        });
    });
});

$(document).ready(function() {
  $(".gamesDiv").on("click", ".researchTeamButton", function() {
    if ($(this).attr('data-line')) {
      var homeTeam = $(this).data("home");
      var awayTeam = $(this).data("away");
      var line = $(this).data("line");

      var matchup ={
        homeTeam: homeTeam,
        awayTeam: awayTeam,
        line: line
      };
      var playerJSON = JSON.stringify(matchup);
      var encodedPlayerJSON = encodeURIComponent(playerJSON);
      var redirectURL = "/researchMLBteam?matchup=" + encodedPlayerJSON;
      window.location.href = redirectURL;
    }

    else{
      var homeTeam = $(this).data("home");
      var awayTeam = $(this).data("away");
      var matchup = {
        homeTeam: homeTeam,
        awayTeam: awayTeam
      };

      var playerJSON = JSON.stringify(matchup);
      var encodedPlayerJSON = encodeURIComponent(playerJSON);
      var redirectURL = "/researchMLBteam?matchup=" + encodedPlayerJSON;
      window.location.href = redirectURL;
  }
  });
});


$(document).ready(function() {
    $(".propsDiv").on("click", ".researchButton", function() {
        var stat = $(this).data("cat");
        var name = $(this).data("name");
        var line = $(this).data("line");
        var spread = $(this).data("spread");
        var space = name.split(" ");
        var fname = space[0];
        var lname = space[1];
        var tot = $(this).data("tot");

        var player = {
            stat: stat,
            num: line,
            fname: fname,
            lname: lname,
            tot: tot,
            spread: spread
        };
        console.log(player);

        var playerJSON = JSON.stringify(player);
        var encodedPlayerJSON = encodeURIComponent(playerJSON);
        var redirectURL = "/researchNBAPlayer?player=" + encodedPlayerJSON;
     //   var redirectURL = "/researchMLB?player=" + encodedPlayerJSON;
        window.location.href = redirectURL;

    });
});

function dropdownFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
  }
  
  // Close the dropdown menu if the user clicks outside of it
  window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
      var dropdowns = document.getElementsByClassName("dropdown-content");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  }

  $(document).ready(function() {
    $(".vote").click(function() {
      // Remove the selected class from all buttons
      $(".vote").removeClass("voted-over voted-under");
      //$(this).siblings(".vote").removeClass("voted-over voted-under");
  
      $(this).addClass(function() {
        return ($(this).attr("id") === "overButton") ? "voted-over" : "voted-under";
      });
    });
  });

  function confirmCancellation() {
    return confirm("Are you sure you want to cancel your subscription? (You will still have access to PropCodes until end of billing period)");
  }

  $(document).ready(function() {
    $(".updateSport").off("click").on("click", function() {
        $(this).siblings(".updateSport").removeClass("button-selected");
        $(this).addClass("button-selected");
        //var button = $(this);
        var parameter = $(this).data("parameter");
        //var propsDiv = button.closest(".container").find(".propsDiv");
        var propsDiv = $('.container .propsDiv');
        var catDiv = $('.container .buttoncontainer');
        console.log(parameter);  
        $.ajax({
            url: "/sportprocess",
            type: "POST",
            data: {parameter: parameter},
            success: function(response) {
                var updatedProps = "<table><thead>";
                updatedProps += "<tr> <th>Player</th> <th>Line</th> <th>PropCodes Score</th> <th>Views</th> <th>Over</th> <th>Under</th> </tr></thead><tbody>";
                $.each(response.content, function(index, row){
                    updatedProps += "<tr>"
                    $.each(row, function(itemIndex, i) {
                      console.log(i);
                        if (itemIndex === 6)
                        {
                           updatedProps += ("<td style='color: green;'>" + i + "</td>")
                        }
                        else if (itemIndex === 7)
                        {
                            updatedProps += ("<td style='color: red;'>" + i + "</td>")
                        }
                        else if (itemIndex != 2 && itemIndex != 3 && itemIndex != 4)
                        {
                            updatedProps += ("<td>" + i + "</td>");
                        }
                    });
                    updatedProps += ("<td><button class='researchButton'");
                    $.each(row, function(itemIndex, i) {
                        if (itemIndex === 0)
                        {
                            updatedProps += (" data-name='" + i + "'");
                        }
                        else if(itemIndex === 1)
                        {
                            updatedProps += (" data-line='" + i + "'");
                        }
                        else if (itemIndex === 2)
                        {
                            updatedProps += (" data-cat='" + i + "'");
                        }
                        else if(itemIndex == 3)
                        {
                          updatedProps += (" data-tot='" + i + "'")
                        }
                        else if(itemIndex == 4)
                        {
                          updatedProps += (" data-spread='" + i + "'")
                        }
                    });
                    updatedProps += ">Research</button></td></tr>";
                });
                updatedProps += "</tbody></table>";
                console.log(updatedProps)
                propsDiv.find("table").html(updatedProps);
                $(".gamescontainer").empty();
                var buttonContainer = $("<div class=buttoncontainer>");
                $.each(response.games, function(num, game)
                {
                  if (num == 0)
                    var button = $(`<button class="updateGame button-selected" data-parameter="` + game + `">` + game + "</button>");
                  else
                    var button = $(`<button class="updateGame" data-parameter="` + game + `">` + game + "</button>");
                  buttonContainer.append(button);
                });
              buttonContainer.append("</div>");
              $(".gamescontainer").append(buttonContainer);
              //var container = $(this).closest('.container');
            //  container.find(".buttoncontainer").empty();
              //$(".container").empty();
              if (parameter == "mlb")
              {
                var newButtonsHTML = `
                    <button class="updateProps button-selected" data-parameter="hrb">Hits+Runs+RBI</button>
                    <button class="updateProps" data-parameter="k">Strikeouts</button>
                    <button class="updateProps" data-parameter="tb">Total Bases</button>
                    <button class="updateProps" data-parameter="r">Runs</button>
                    <button class="updateProps" data-parameter="era">Earned Runs Allowed</button>
                    <button class="updateProps" data-parameter="hits">Hits Allowed</button>
                    <button class="updateProps" data-parameter="outs">Pitching Outs</button>
                `;
              }
              else if (parameter == "nba")
              {
                var newButtonsHTML = `
                  <button class="updateProps button-selected" data-parameter="points">Points</button>
                  <button class="updateProps" data-parameter="rebounds">Rebounds</button>
                  <button class="updateProps" data-parameter="assists">Assists</button>
                  <button class="updateProps" data-parameter="3-pt">3-PT Made</button>
                  <button class="updateProps" data-parameter="pra">Pts+Reb+Ast</button>
                  `;
              }
              catDiv.html(newButtonsHTML);
              //$(".container").append(newButtonsHTML);
             // container.find(".buttoncontainer").html(newButtonsHTML);
            //  $(".container").html(newButtonsHTML);

            },
            error: function(error){
                console.log(error);
            }
        });
    });
  });