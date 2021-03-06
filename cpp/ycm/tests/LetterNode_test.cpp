// Copyright (C) 2016 ycmd contributors
//
// This file is part of ycmd.
//
// ycmd is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// ycmd is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with ycmd.  If not, see <http://www.gnu.org/licenses/>.

#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include "LetterNode.h"

namespace YouCompleteMe {

using ::testing::AllOf;
using ::testing::ElementsAre;
using ::testing::IsNull;
using ::testing::Property;
using ::testing::StrEq;

TEST( LetterNodeTest, AsciiText ) {
  LetterNode root_node( "ascIi_texT" );
  EXPECT_THAT( root_node,
    AllOf( Property( &LetterNode::Index, -1 ),
           Property( &LetterNode::LetterIsUppercase, false ) ) );

  const std::list< LetterNode *> *list = root_node.NodeListForLetter( 'i' );
  EXPECT_THAT( *list, ElementsAre(
    AllOf( Property( &LetterNode::Index, 3 ),
           Property( &LetterNode::LetterIsUppercase, true ) ),
    AllOf( Property( &LetterNode::Index, 4 ),
           Property( &LetterNode::LetterIsUppercase, false ) ) ) );

  LetterNode *node = list->front();

  list = node->NodeListForLetter( 'i' );
  EXPECT_THAT( *list, ElementsAre(
    AllOf( Property( &LetterNode::Index, 4 ),
           Property( &LetterNode::LetterIsUppercase, false ) ) ) );

  list = node->NodeListForLetter( 't' );
  EXPECT_THAT( *list, ElementsAre(
    AllOf( Property( &LetterNode::Index, 6 ),
           Property( &LetterNode::LetterIsUppercase, false ) ),
    AllOf( Property( &LetterNode::Index, 9 ),
           Property( &LetterNode::LetterIsUppercase, true ) ) ) );

  list = node->NodeListForLetter( 'c' );
  EXPECT_THAT( list, IsNull() );
}


TEST( LetterNodeTest, ThrowOnNonAsciiCharacters ) {
  // UTF-8 characters representation:
  //   ¢: \xc2\xa2
  //   €: \xe2\x82\xac
  //   𐍈: \xf0\x90\x8d\x88
  ASSERT_THROW( LetterNode root_node( "uni¢𐍈d€" ), std::out_of_range );
  try {
    LetterNode root_node( "uni¢𐍈d€" );
  } catch ( std::out_of_range error ) {
    EXPECT_THAT( error.what(), StrEq( "array<>: index out of range" ) );
  }
}

} // namespace YouCompleteMe
